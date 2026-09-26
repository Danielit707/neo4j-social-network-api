from app.database import get_db
from typing import Optional, Dict

def create_user_node(username: str, email: str, password: str, full_name: Optional[str]=None):
    with get_db() as session:
        session.run(
            """
            CREATE (u:User {username:$username, email:$email, password:$password, full_name:$full_name})
            """,
            username=username, email=email, password=password, full_name=full_name
        )

def get_user_by_email_record(email: str):
    with get_db() as session:
        res = session.run("MATCH (u:User {email:$email}) RETURN u", email=email)
        return res.single()

def get_user_node_props_by_email(email: str):
    rec = get_user_by_email_record(email)
    if not rec:
        return None
    node = rec["u"]
    props = dict(node._properties)
    props["labels"] = list(node.labels)
    props["id"] = node.id
    return props

def create_friendship(user_email: str, friend_email: str, bidir: bool=True):
    with get_db() as session:
        if bidir:
            session.run("""
            MATCH (a:User {email:$user_email}), (b:User {email:$friend_email})
            MERGE (a)-[:FRIENDS_WITH]->(b)
            MERGE (b)-[:FRIENDS_WITH]->(a)
            """, user_email=user_email, friend_email=friend_email)
        else:
            session.run("""
            MATCH (a:User {email:$user_email}), (b:User {email:$friend_email})
            MERGE (a)-[:FOLLOWS]->(b)
            """, user_email=user_email, friend_email=friend_email)

def create_post(author_email: str, content: str, media_url: Optional[str]=None):
    with get_db() as session:
        result = session.run("""
        MATCH (u:User {email:$email})
        CREATE (p:Post {id: randomUUID(), content:$content, media:$media, created_at: datetime()})
        CREATE (u)-[:POSTED]->(p)
        RETURN p
        """, email=author_email, content=content, media=media_url)
        return result.single()

def comment_on_post(author_email: str, post_id: str, content: str):
    with get_db() as session:
        res = session.run("""
        MATCH (u:User {email:$email}), (p:Post {id:$post_id})
        CREATE (c:Comment {id: randomUUID(), content:$content, created_at: datetime()})
        CREATE (u)-[:COMMENTED]->(c)
        CREATE (c)-[:ON]->(p)
        RETURN c
        """, email=author_email, post_id=post_id, content=content)
        return res.single()

def add_interest_to_user(user_email: str, interest_name: str):
    with get_db() as session:
        session.run("""
        MATCH (u:User {email:$email})
        MERGE (i:Interest {name:$interest})
        MERGE (u)-[:INTERESTED_IN]->(i)
        """, email=user_email, interest=interest_name)

def get_user_network(email: str, depth: int = 2):
    with get_db() as session:
        q = """
        MATCH (u:User {email:$email})-[*1..$depth]-(n)
        WITH collect(distinct n) + u as nodes
        UNWIND nodes as x
        OPTIONAL MATCH (x)-[r]-(y)
        WHERE y IN nodes
        RETURN collect(distinct x) as nodes, collect(distinct r) as rels
        """
        res = session.run(q, email=email, depth=depth)
        record = res.single()
        if not record:
            return {"nodes": [], "rels": []}
        nodes = []
        for node in record["nodes"]:
            props = dict(node._properties)
            props["labels"] = list(node.labels)
            props["id"] = node.id
            nodes.append(props)
        rels = []
        for r in record["rels"]:
            if r is None:
                continue
            rels.append({
                "id": r.id,
                "type": r.type,
                "start": r.start_node.id,
                "end": r.end_node.id,
                "props": dict(r._properties)
            })
        return {"nodes": nodes, "rels": rels}
