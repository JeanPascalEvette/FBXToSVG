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

    rotation =  45 
    rotation = rotation * 3.1415926 / 180

    sdk_manager, scene = FbxCommon.InitializeSdkObjects()
    if not FbxCommon.LoadScene(sdk_manager, scene, os.getcwd()+pathToFbx):
        print("error in LoadScene. File found : %s" % os.path.isfile(pathToFbx))
        print("Current working directory : %s" % os.getcwd())
        print("file directory : %s" % os.getcwd()+pathToFbx)
        
    svgContents = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n<!DOCTYPE svg PUBLIC '-//W3C//DTD SVG 1.0//EN' 'http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd'>\n<svg width='280' height='280'\nxmlns='http://www.w3.org/2000/svg'\nxmlns:xlink='http://www.w3.org/1999/xlink'\nonload='init(evt)' >"

    svgContents += "\n\n<style>\n\tsvg\n{\nmargin-left:100px;\nmargin-top:100px;\n}\n.edge{\n\t\tstroke: black;\n\t\tstroke-width: 1;\n\t}\n\t.button{\n\t\tfill: #2060dd;\n\t\tstroke: #2580ff;\n\t\tstroke-width: 1;\n\t}\n\t.button:hover{\n\t\tstroke-width: 3;\n\t}\n</style>"

    svgContents += "\n<script type='text/ecmascript'> \n<![CDATA[\n"

    for u in range(scene.GetNodeCount()):
        node = scene.GetNode(u)
        for i in range(node.GetChildCount()):
            child = node.GetChild(i)
            svgContents += "edges = ["
            for m in range(child.GetMesh().GetMeshEdgeCount()):
                startIndex, endIndex = child.GetMesh().GetMeshEdgeVertices(m)
                svgContents += "[" + str(startIndex) + "," + str(endIndex) + "],"
            svgContents = svgContents[:-1] + "]\n"

            
            svgContents += "faces = ["
            for m in range(child.GetMesh().GetPolygonCount()):
                svgContents += "["
                for n in range(child.GetMesh().GetPolygonSize(m)):
                    svgContents += str(child.GetMesh().GetPolygonVertex(m,n))+","
                svgContents = svgContents[:-1] + "],"
            svgContents = svgContents[:-1] + "]\n"

        

        
            xCoords = "x_coords = ["
            yCoords = "y_coords = ["
            zCoords = "z_coords = ["
            smallestControlPoint = 0
            for i in range(child.GetMesh().GetControlPointsCount()):
                if(smallestControlPoint > child.GetMesh().GetControlPoints()[i][0]):
                    smallestControlPoint = child.GetMesh().GetControlPoints()[i][0]
                if(smallestControlPoint > child.GetMesh().GetControlPoints()[i][1]):
                    smallestControlPoint = child.GetMesh().GetControlPoints()[i][1]
                if(smallestControlPoint > child.GetMesh().GetControlPoints()[i][2]):
                    smallestControlPoint = child.GetMesh().GetControlPoints()[i][2]
            smallestControlPoint -= 30
            for i in range(child.GetMesh().GetControlPointsCount()):
                xCoords += str(child.GetMesh().GetControlPoints()[i][0] - smallestControlPoint) + ","
                yCoords += str(child.GetMesh().GetControlPoints()[i][1] - smallestControlPoint) + ","
                zCoords += str(child.GetMesh().GetControlPoints()[i][2] - smallestControlPoint) + ","
            
            xCoords = xCoords[:-1] + "];\n"
            yCoords = yCoords[:-1] + "];\n"
            zCoords = zCoords[:-1] + "];\n"

            svgContents += xCoords + yCoords + zCoords

            svgContents += "\n\ncentre_x = "+str(-smallestControlPoint)+";\ncentre_y = "+str(-smallestControlPoint)+";\ncentre_z = "+str(-smallestControlPoint)+";\n\n\n"
            svgContents += "function init(evt)\n{\n\tif ( window.svgDocument == null )\n\t{\n\t\tsvgDocument = evt.target.ownerDocument;\n\t}\n\trotateAboutX("+str(rotation)+");\n\trotateAboutY("+str(rotation)+");\n\tdrawBox();\n}"
            svgContents += "\n\n\nfunction drawBox()\n{\n\tfor(var i=0; i<faces.length; i++)\n\t{\n\t\tface = svgDocument.getElementById('face-'+i);\n\t\tface.setAttributeNS(null, 'd', 'm'+x_coords[faces[i][0]]+' '+y_coords[faces[i][0]] + ' ' + 'L'+x_coords[faces[i][1]]+' '+y_coords[faces[i][1]] + ' ' + 'L'+x_coords[faces[i][2]]+' '+y_coords[faces[i][2]] + ' ' + 'L'+x_coords[faces[i][3]]+' '+y_coords[faces[i][3]] + ' ' + 'Z');\n\t}\n}"
            svgContents += "\n\n\nfunction rotateAboutX(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\ty = y_coords[i] - centre_y;\n\t\tz = z_coords[i] - centre_z;\n\t\td = Math.sqrt(y*y + z*z);\n\t\ttheta  = Math.atan2(y, z) + radians;\n\t\ty_coords[i] = centre_y + d * Math.sin(theta);\n\t\tz_coords[i] = centre_z + d * Math.cos(theta);\n\t}\n}"
            svgContents += "\n\n\nfunction rotateAboutY(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\tx = x_coords[i] - centre_x;\n\t\tz = z_coords[i] - centre_z;\n\t\td = Math.sqrt(x*x + z*z);\n\t\ttheta  = Math.atan2(x, z) + radians;\n\t\tx_coords[i] = centre_x + d * Math.sin(theta);\n\t\tz_coords[i] = centre_z + d * Math.cos(theta);\n\t}\n\tdrawBox();\n}"

            svgContents += "\n\n]]>\n</script>\n\n"

            for n in range (child.GetMesh().GetPolygonCount()):
                for k in range(child.GetMesh().GetPolygonVertexCount()):
                    poly = FbxCommon.FbxPropertyDouble3(child.GetMesh().FindProperty("Color")).Get()
                svgContents += "\n<path stroke='" + str('#%02x%02x%02x' % (clamp(poly[0]*255), clamp(poly[1]*255), clamp(poly[2]*255))) + "' fill='transparent' id='face-"+str(n)+"' d=''/>"
            
            svgContents += "\n\n</svg>"


    with open('myFile.svg', 'w') as file_:
        file_.write(svgContents)
    
def clamp(x): 
  return max(0, min(x, 255))    

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




