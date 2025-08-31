from app import tools

def test_list_tools():
    tools_list = tools.list_tools()
    assert any(t["name"] == "get_time" for t in tools_list)

def test_get_time():
    t = tools.get_time()
    assert "time" in t