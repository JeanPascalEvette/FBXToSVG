import FbxCommon
import math
import json

import time
import BaseHTTPServer
import os
import urllib



# example of a python class
  
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

  def do_POST(s):
                        content_len = int(s.headers.getheader('content-length', 0))
                        post_body = json.loads(s.rfile.read(content_len))
                        test = post_body['head_commit']
                        if(post_body['head_commit'] == None):
                            return;
                        message = post_body['head_commit']['message']
                        if(len(message.split(' ')) != 2):
                            return;
                        command = message.split(' ')[0]
                        arg = message.split(' ')[1]
                        if(command == 'adding' and arg[:4] == 'http'):
                            fileName = "FBX/" + os.path.basename(arg)
                            fileNameTest = fileName
                            num = 1
                            while(os.path.isfile(fileNameTest)):
                                fileNameTest = fileName[:-4] + "(" + str(num) + ").fbx"
                                num = num + 1
                            fileName = fileNameTest
                            urllib.urlretrieve(arg, fileName)



                        s.send_response(200)
                        s.send_header('Content-type',        'text/html')
                        s.end_headers() 
        
                        s.wfile.write("OK")
  def do_GET(s):
       
    if s.path.endswith(".svg"):
                        f=open(os.getcwd()+s.path)
                        s.send_response(200)
                        s.send_header('Content-type',        'image/svg+xml')
                        s.end_headers()
                        s.wfile.write(f.read())
                        f.close()
                        return
    if s.path.endswith(".ico"):
                        s.send_response(404)
                        s.send_header('Content-type',        'image/ico')
                        s.end_headers()
                        return

    if(s.path == "/favicon.ico" or s.path == "/test.svg"):
        return
    """Respond to a GET request."""
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    s.wfile.write("<html><head><title>Title goes here.</title>")
    s.wfile.write("<style type='text/css'>object\n{\nborder : 1px inset lightgray;\n}\n.thumbnail\n{\nmargin-right:10px;\nmargin-bottom:10px;\n}\n</style></head>")
    s.wfile.write("<body>")
    
    
    for dirname, dirnames, filenames in os.walk('FBX'):
        for filename in filenames:
            drawLines("/FBX/"+filename)
            s.wfile.write("<object class='thumbnail' width='150px' height='150px' data=\"SVG/"+filename[:-3]+"svg\" type=\"image/svg+xml\"></object>")
    s.wfile.write("</body></html>")
    

def drawLines(pathToFbx):
    rotation =  -45 
    rotation = rotation * 3.1415926 / 180

    sdk_manager, scene = FbxCommon.InitializeSdkObjects()
    if not FbxCommon.LoadScene(sdk_manager, scene, os.getcwd()+pathToFbx ):
        print("error in LoadScene. File found : %s" % os.path.isfile(pathToFbx))
        print("Current working directory : %s" % os.getcwd())
        print("file directory : %s" % os.getcwd()+pathToFbx)
        
    svgContents = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n<!DOCTYPE svg PUBLIC '-//W3C//DTD SVG 1.0//EN' 'http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd'>\n<svg width='100%' height='100%' viewBox='0 0 0 0' preserveAspectRatio='xMidYMid meet' \nxmlns='http://www.w3.org/2000/svg'\nxmlns:xlink='http://www.w3.org/1999/xlink'\nonload='init(evt)'>"

    svgContents += "\n\n<style>\n\tsvg\n{\n}\n.edge{\n\t\tstroke: black;\n\t\tstroke-width: 1;\n\t}\n\t.button{\n\t\tfill: #2060dd;\n\t\tstroke: #2580ff;\n\t\tstroke-width: 1;\n\t}\n\t.button:hover{\n\t\tstroke-width: 3;\n\t}\n</style>"

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
                
            svgContents += "depth = ["
            for m in range(child.GetMesh().GetPolygonCount()):
                svgContents += "0,"
            svgContents = svgContents[:-1] + "];\n"

        
            xCoords = "x_coords = ["
            yCoords = "y_coords = ["
            zCoords = "z_coords = ["
            smallestControlPointX = 0
            smallestControlPointY = 0
            smallestControlPointZ = 0
            for i in range(child.GetMesh().GetControlPointsCount()):
                if(smallestControlPointX > child.GetMesh().GetControlPoints()[i][0]):
                    smallestControlPointX = child.GetMesh().GetControlPoints()[i][0]
                if(smallestControlPointY > child.GetMesh().GetControlPoints()[i][1]):
                    smallestControlPointY = child.GetMesh().GetControlPoints()[i][1]
                if(smallestControlPointZ > child.GetMesh().GetControlPoints()[i][2]):
                    smallestControlPointZ = child.GetMesh().GetControlPoints()[i][2]


            for i in range(child.GetMesh().GetControlPointsCount()):
                xCoords += str(child.GetMesh().GetControlPoints()[i][0] - smallestControlPointX) + ","
                yCoords += str(child.GetMesh().GetControlPoints()[i][1] - smallestControlPointY) + ","
                zCoords += str(child.GetMesh().GetControlPoints()[i][2] - smallestControlPointZ) + ","
            
            xCoords = xCoords[:-1] + "];\n"
            yCoords = yCoords[:-1] + "];\n"
            zCoords = zCoords[:-1] + "];\n"

            svgContents += xCoords + yCoords + zCoords

            svgContents += "\n\ncentre_x = "+str(-smallestControlPointX)+";\ncentre_y = "+str(-smallestControlPointY)+";\ncentre_z = "+str(-smallestControlPointZ)+";\n\n\n\n\tvar minX = -999;\n\tvar minY = -999;\n\tvar maxX = -999;\n\tvar maxY = -999;\n\n"
            svgContents += "function init(evt)\n{\n\tif ( window.svgDocument == null )\n\t{\n\t\tsvgDocument = evt.target.ownerDocument;\n\t}\n\trotateAboutZ("+str(rotation)+");\n\trotateAboutX("+str(rotation)+");\n\tcalculateDepth()\n\tdrawBox();\n\tsetViewBox();\nif(minX < 0 || minY < 0)\n{\n\tfixCoords();\n\tdrawBox();\n\tsetViewBox();\n}}"
            
            svgContents += "\n\n\nfunction setViewBox()\n{\n\tminX = -999;\n\tminY = -999;\n\tmaxX = -999;\n\tmaxY = -999;\n\t\n\tfor(var i = 0; i < x_coords.length; i++)\n\t{\n\t\tif(minX == -999 || x_coords[i] < minX)\n\t\t\tminX = x_coords[i];\n\t\tif(minY == -999 || y_coords[i] < minY)\n\t\t\tminY = y_coords[i];\n\t\tif(maxX == -999 || x_coords[i] > maxX)\n\t\t\tmaxX = x_coords[i];\n\t\tif(maxY == -999 || y_coords[i] > maxY)\n\t\t\tmaxY = y_coords[i];\n\t}\n\tshape = document.getElementsByTagName('svg')[0];\n\tshape.setAttribute('viewBox', minX+' '+ minY+' '+ maxX +' '+maxY);\n}"
            svgContents += "\n\n\nfunction fixCoords()\n{\n\tif(minX < 0)\n\t{\n\t\tcentre_x += -minX;\n\t\tfor(var i = 0; i < x_coords.length;i++)\n\t\t{\n\t\t\tx_coords[i] += -minX;\n\t\t}\n\t}\n\tif(minY < 0)\n\t{\n\t\tcentre_y += -minY;\n\t\tfor(var i = 0; i < y_coords.length;i++)\n\t\t{\n\t\t\ty_coords[i] += -minY;\n\t\t}\n\t}\n}"            
            svgContents += "\n\n\nfunction calculateDepth()\n{\n\tvar facesDepth = Array(faces.length);\n\tfor(var i = 0; i < faces.length; i++)\n\t{\n\t\tvar currentDepth = 0;\n\t\tfor(var u = 0; u < faces[i].length; u ++)\n\t\t{\n\t\t\tcurrentDepth += z_coords[faces[i][u]];\n\t\t}\n\t\tcurrentDepth /= faces[i].length;\n\t\tfacesDepth[i] = currentDepth;\n\t}\n\tfor(var i = 0; i < depth.length; i++)\n\t{\n\t\tvar smallest = -1;\n\t\tfor(var u = 0; u < facesDepth.length; u++)\n\t\t{\n\t\t\tif(facesDepth[u] != -99999 && (smallest == -1 || facesDepth[smallest] > facesDepth[u]))\n\t\t\t\tsmallest = u;\n\t\t}\n\t\tdepth[i] = smallest;\n\t\tfacesDepth[smallest] = -99999;\n\t}\n}"
            svgContents += "\n\n\nfunction drawBox()\n{\n\tfor(var i=0; i<depth.length; i++)\n\t{\n\t\tface = svgDocument.getElementById('face-'+i);\n\t\tvar d = 'm'+x_coords[faces[depth[i]][0]]+' '+y_coords[faces[depth[i]][0]];\n\t\tfor(var u = 1; u < faces[depth[i]].length; u++)\n\t\t{\n\t\t\td+= ' ' + 'L'+x_coords[faces[depth[i]][u]]+' '+y_coords[faces[depth[i]][u]];\n\t\t}\n\t\td+= ' Z';\n\t\tface.setAttributeNS(null, 'd', d);\n\t}\n}"
            
            
            svgContents += "\n\n\nfunction rotateAboutX(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\ty = y_coords[i] - centre_y;\n\t\tz = z_coords[i] - centre_z;\n\t\td = Math.sqrt(y*y + z*z);\n\t\ttheta  = Math.atan2(y, z) + radians;\n\t\ty_coords[i] = centre_y + d * Math.sin(theta);\n\t\tz_coords[i] = centre_z + d * Math.cos(theta);\n\t}\n}"
            svgContents += "\n\n\nfunction rotateAboutY(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\tx = x_coords[i] - centre_x;\n\t\tz = z_coords[i] - centre_z;\n\t\td = Math.sqrt(x*x + z*z);\n\t\ttheta  = Math.atan2(x, z) + radians;\n\t\tx_coords[i] = centre_x + d * Math.sin(theta);\n\t\tz_coords[i] = centre_z + d * Math.cos(theta);\n\t}\n}"
            svgContents += "\n\n\nfunction rotateAboutZ(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\tx = x_coords[i] - centre_x;\n\t\ty = y_coords[i] - centre_y;\n\t\td = Math.sqrt(x*x + y*y);\n\t\ttheta  = Math.atan2(x, y) + radians;\n\t\tx_coords[i] = centre_x + d * Math.sin(theta);\n\t\ty_coords[i] = centre_y + d * Math.cos(theta);\n\t}\n}"

            svgContents += "\n\n]]>\n</script>\n\n"

            for n in range (child.GetMesh().GetPolygonCount()):
                poly = FbxCommon.FbxPropertyDouble3(child.GetMesh().FindProperty("Color")).Get()
                r = clamp(poly[0] * 255 - poly[0] * 0.4 * ((n+0.0) / child.GetMesh().GetPolygonCount()) * 255)
                g = clamp(poly[1] * 255 - poly[1] * 0.4 * ((n+0.0) / child.GetMesh().GetPolygonCount()) * 255)
                b = clamp(poly[2] * 255 - poly[2] * 0.4 * ((n+0.0) / child.GetMesh().GetPolygonCount()) * 255)
                svgContents += "\n<path stroke='" + str('#%02x%02x%02x' % (r, g, b)) + "' fill='" + str('#%02x%02x%02x' % (r, g, b)) + "' id='face-"+str(n)+"' d=''/>"
            
            svgContents += "\n\n</svg>"

    svgFileName = 'SVG' + (pathToFbx[4:])[:-3] + 'svg'        
    with open(svgFileName, 'w') as file_:
        file_.write(svgContents)
    
def clamp(x): 
  return max(0, min(x, 255))    


httpd = BaseHTTPServer.HTTPServer(("localhost", 8000), MyHandler)
httpd.serve_forever()




