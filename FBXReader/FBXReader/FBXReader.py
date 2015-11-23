import FbxCommon
import svgwrite


import time
import BaseHTTPServer
import os

# example of a python class
 
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):


  def do_GET(s):

    if s.path.endswith(".svg"):
                        f=open(os.getcwd()+s.path)
                        s.send_response(200)
                        s.send_header('Content-type',        'image/svg+xml')
                        s.end_headers()
                        s.wfile.write(f.read())
                        f.close()
                        return

    if(s.path == "/favicon.ico" or s.path == "/test.svg"):
        return
    """Respond to a GET request."""
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    s.wfile.write("<html><head><title>Title goes here.</title></head>")
    s.wfile.write("<body><p>This is a test.</p>")


    
    s.wfile.write("<p>You accessed path: %s</p>" % s.path)
    s.wfile.write("<p>Vertices Count: %s</p>" % getVerticesCount(s.path))
    
    drawLines(s.path)

    s.wfile.write("<object data=\"test.svg\" type=\"image/svg+xml\"></object>")
    s.wfile.write("</body></html>")
    

def drawLines(pathToFbx):
    sdk_manager, scene = FbxCommon.InitializeSdkObjects()
    if not FbxCommon.LoadScene(sdk_manager, scene, os.getcwd()+pathToFbx):
        print("error in LoadScene. File found : %s" % os.path.isfile(pathToFbx))
        print("Current working directory : %s" % os.getcwd())
        print("file directory : %s" % os.getcwd()+pathToFbx)
        
    svgContents = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n<!DOCTYPE svg PUBLIC '-//W3C//DTD SVG 1.0//EN' 'http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd'>\n<svg width='280' height='280'\nxmlns='http://www.w3.org/2000/svg'\nxmlns:xlink='http://www.w3.org/1999/xlink'\nonload='init(evt)' >\n<script type='text/ecmascript'> \n<![CDATA[\n"
    for u in range(scene.GetNodeCount()):
        node = scene.GetNode(u)
        for i in range(node.GetChildCount()):
            child = node.GetChild(i)
            svgContents += "edges = ["
            for m in range(child.GetMesh().GetPolygonCount()):
                svgContents += "["
                for n in range(child.GetMesh().GetPolygonSize(m)):
                    svgContents += str(child.GetMesh().GetPolygonVertex(m,n))+","
                svgContents = svgContents[-1:] + "],"
            svgContents = svgContents[-1:] + "]\n"

        
            xCoords = "["
            yCoords = "["
            zCoords = "["
            for i in range(child.GetMesh().GetControlPointsCount()):
                xCoords += str(child.GetMesh().GetControlPoints()[i][0]) + ","
                yCoords += str(child.GetMesh().GetControlPoints()[i][1]) + ","
                zCoords += str(child.GetMesh().GetControlPoints()[i][2]) + ","
            
            xCoords = xCoords[-1:] + "];\n"
            yCoords = yCoords[-1:] + "];\n"
            zCoords = zCoords[-1:] + "];\n"

            svgContents += xCoords + yCoords + zCoords


    with open('myFile.svg', 'w') as file_:
        file_.write(svgContents)
    
    

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
            polCOunt = ""
            for z in range(child.GetMesh().GetMeshEdgeCount()):
                startIndex = -1
                endIndex = -1
                startIndex, endIndex = child.GetMesh().GetMeshEdgeVertices(z)
                startVector = child.GetMesh().GetControlPointAt(startIndex)
                endVector = child.GetMesh().GetControlPointAt(endIndex)
                


                polList = "<br/>"

                for m in range(child.GetMesh().GetPolygonCount()):
                    polList += "("
                    for n in range(child.GetMesh().GetPolygonSize(m)):
                        polList += str(child.GetMesh().GetControlPointAt(child.GetMesh().GetPolygonVertex(m,n)))+","
                    polList += ")<br/>"


                lineList += "<br/>" + str(startVector) + " - " + str(endVector)
            child.GetMesh().EndGetMeshEdgeVertices()
            attr_type = child.GetNodeAttribute().GetAttributeType()

            if attr_type == FbxCommon.FbxNodeAttribute.eMesh:
                print(child)
    return (str(counter) + " edge count " + str(lineCounter) + "-" + polCOunt + polList + lineList )
    

httpd = BaseHTTPServer.HTTPServer(("localhost", 8000), MyHandler)
httpd.serve_forever()




