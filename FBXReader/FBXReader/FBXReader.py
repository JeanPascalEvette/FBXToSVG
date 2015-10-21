import FbxCommon

import time
import BaseHTTPServer
import os

# example of a python class
 
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):


  def do_GET(s):
    if(s.path == "/favicon.ico"):
        return
    """Respond to a GET request."""
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    s.wfile.write("<html><head><title>Title goes here.</title></head>")
    s.wfile.write("<body><p>This is a test.</p>")





    
    s.wfile.write("<p>You accessed path: %s</p>" % s.path)
    s.wfile.write("<p>Vertices Count: %s</p>" % getVerticesCount(s.path))
    s.wfile.write("</body></html>")
    

def getVerticesCount(pathToFbx):
    if(pathToFbx.substring(0,1) == "/"):
        pathToFbx = pathToFbx.substring(1,pathToFbx.length())
    sdk_manager, scene = FbxCommon.InitializeSdkObjects()
    if not FbxCommon.LoadScene(sdk_manager, scene, pathToFbx):
        print("error in LoadScene. File found : %s" % os.path.isfile(pathToFbx))
        print("Current working directory : %s" % os.getcwd())

        
    counter = 0
    for u in range(scene.GetNodeCount()):
        node = scene.GetNode(u)
        for i in range(node.GetChildCount()):
            child = node.GetChild(i)
            counter += child.GetMesh().GetPolygonVertexCount()
            attr_type = child.GetNodeAttribute().GetAttributeType()

            if attr_type == FbxCommon.FbxNodeAttribute.eMesh:
                print(child)
    return counter
    

httpd = BaseHTTPServer.HTTPServer(("10.240.0.2", 8000), MyHandler)
httpd.serve_forever()




