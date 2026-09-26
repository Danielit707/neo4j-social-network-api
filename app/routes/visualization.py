from fastapi import APIRouter, Response
from app.models.graph_model import get_user_network
from pyvis.network import Network
import tempfile, os

router = APIRouter()

@router.get("/network/{email}")
def network_vis(email: str):
    data = get_user_network(email, depth=2)
    net = Network(height="700px", width="100%", notebook=False)
    for n in data["nodes"]:
        nid = n["id"]
        label = n.get("username") or n.get("full_name") or ",".join(n.get("labels", []))
        title = "<br>".join(f"{k}: {v}" for k,v in n.items() if k not in ("id","labels"))
        net.add_node(nid, label=label, title=title)
    for r in data["rels"]:
        net.add_edge(r["start"], r["end"], title=r["type"])
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.show(tmp.name)
    tmp.close()
    with open(tmp.name, "r", encoding="utf-8") as f:
        html = f.read()
    os.unlink(tmp.name)
    return Response(content=html, media_type="text/html")
