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
    sdk_manager, scene = FbxCommon.InitializeSdkObjects()
    if not FbxCommon.LoadScene(sdk_manager, scene, os.getcwd()+pathToFbx):
        print("error in LoadScene. File found : %s" % os.path.isfile(pathToFbx))
        print("Current working directory : %s" % os.getcwd())
        print("file directory : %s" % os.getcwd()+pathToFbx)
        
    counter = 0
    lineCounter = 0
    lineList = ""
    for u in range(scene.GetNodeCount()):
        node = scene.GetNode(u)
        for i in range(node.GetChildCount()):
            child = node.GetChild(i)
            counter += child.GetMesh().GetPolygonVertexCount()
            lineCounter += child.GetMesh().GetMeshEdgeCount()
            child.GetMesh().BeginGetMeshEdgeVertices()
            for z in range(child.GetMesh().GetMeshEdgeCount()):
                startIndex = -1
                endIndex = -1
                startIndex, endIndex = child.GetMesh().GetMeshEdgeVertices(z)
                startVector = child.GetMesh().GetControlPointAt(startIndex)
                endVector = child.GetMesh().GetControlPointAt(endIndex)
                lineList += "<br/>" + str(startVector) + " - " + str(endVector)
            child.GetMesh().EndGetMeshEdgeVertices()
            attr_type = child.GetNodeAttribute().GetAttributeType()

            if attr_type == FbxCommon.FbxNodeAttribute.eMesh:
                print(child)
    return (str(counter) + " edge count " + str(lineCounter) + lineList)
    

httpd = BaseHTTPServer.HTTPServer(("localhost", 8000), MyHandler)
httpd.serve_forever()




