<h1>Python FBX-Parser - Tools and Middleware Assignment 2</h1>
 
This is the write-up for the Tools and Middleware second coursework assignment.  The project was to create an FBX parser that would read a directory full of FBX files and create corresponding SVG files which are displayed as thumbnails on a webpage.  The group for this project consisted of Mircea Catana, Jean-Pascal Evette and Adam Joyce.  We chose to implement the project a number of different ways.  Due to having several implementations, throughout the write-up I will not reference specific functions, but instead focus on the different steps required to achieve the result.

<h2>Method 1: SVG with ECMAScript</h2>

This section focuses on the method of generating the SVG files with an ECMAScript to perform all the required actions on the models being drawn. 
 
We begin by using the ‘Python FBX’ binding to parse each of the FBX files found in a directory.  For each file an FBX model was selected.  We obtain the mesh face data for each model, storing it as a string ready to be written into the ECMAScript generated in the SVG file.  The data is stored as an array with each element being another array of four vertex control point indices.  An empty depth array with a size corresponding to the number of faces in the model is also generated.  This is to be used to help determine the different depths of each face in the model and thus the order in which they should be drawn.
 
To use these face vertex control point indices to both draw and manipulate the model we also need to store the x, y and z coordinates of the model.  Each of these are stored in a separate array, using their smallest values as an offset to ensure all coordinate values are positive.  This results in the entire model being displayed within the viewable bounds of the page.  The central x, y, and z coordinates are also taken so that the models can be correctly rotated to a desired position.
 
The remaining code written into the ECMAScript is a series of functions that manipulate how the model is drawn and viewed.  We begin by rotating the model’s coordinates into an appropriate position around the required axes.  Another of these functions stretches the model to fit the full SVG window.
 
Before our SVG model image can be constructed, we must determine the order in which the faces should be drawn.  We do this by sorting the faces by their depth, and drawing the closest faces first.  Initially, we compute a mean depth value for each face by summing the z coordinates for each vertex in each face and dividing by the number of vertices.  These values are stored in an array and used to determine the closest faces from the viewing angle.  The closest face’s face array indices are stored first in the depth array we wrote into the script earlier.  This way when building the attributes of the SVG path elements to draw each face, we are able to use the index values stored in the depth array to identify which face stored in the face array we should be dealing with first.
 
The colouring of each face on the model is dealt with in our Python script when we construct the string of path elements to be written in the SVG file.  Since we are storing the faces by depth in the ECMAScript, we are in need of one path per face to differentiate their colours from one another.  We construct an RGB value for each face by slightly altering the original colour of the FBX model.  These values are used to define both the stroke and fill attributes of each of the path elements.  This produces a simplistic shading effect that differentiates each face from one another when the image is viewed.

To conclude the generation of our SVG file we take the concatenation of each of the above mentioned content strings and write it into an appropriately named and located SVG file.
 
The web-page is served up using a simple Python webserver which takes the FBX file paths and generates an SVG file for each.  These SVG file images are formatted into small thumbnail-sized images that can be viewed when accessing the server.

This application can also make use of a GitHub webhook to upload new pictures into the project. The webhook is designed to constantly monitor for new commits.  Whenever a commit is created, the webhook creates a POST request which is sent to the webpage.  This request contains information about the commit stored as a JSON object. In addition to the do_GET function, a do_POST function is implemented to handle the incoming requests from the webhook.  This function catches the comment from the latest commit and ensures that it conforms with the expected format for uploading new images.  If no problem arises, the FBX file linked in the comment will be downloaded and placed into the appropriate FBX folder.  The next time a user opens the page, the corresponding new SVG file will be created and its thumbnail will be displayed.

![FBX Folder](http://www.jeanpascalevette.com/misc/GitHubPics/FBX.PNG)
![FBX Folder](http://www.jeanpascalevette.com/misc/GitHubPics/SVG.PNG)
![FBX Folder](http://www.jeanpascalevette.com/misc/GitHubPics/output.PNG)

<h2>Method 2: SVG directly from Python</h2>

The second method focuses on generating the SVG directly from the python script that makes use of the FBX SDK to read the model’s vertices.

The method is quite similar to the one before with the simple change in the fact that the model transformations are done by pre-set matrices and vectors in the python file. All of the needed data is computed at the start of the program and will be used to transform every vertex of the mesh into “camera space”.

After this stage, vertices are processed on a polygon level. This must be done because the FBX file format stores all the vertices of a mesh in a single array and performs an XOR with 1 for the last vertex in the current polygon to mark it as an ending tag. The current implementation can handle meshes composed of triangles and quads, leaving out any polygon with a higher number of vertices. After the polygons have been stored in an array they are sorted based on their z-value with regards to the viewing ray. This is done similarly to the way it was implemented in Method 1. Namely, they are sorted ascendingly based on the average z position of every vertex in the polygon.

Finally, after z-ordering, the polygons are written to an svg file rendering each of them inside a <polygon> element with an increasing shade of green colouring to give the impression of a diffuse lighting model. 

<h2>References</h2>

The main reference source materials that we used for this project is listed below:

http://www.petercollingridge.co.uk/blog/rotating-3d-svg-cube
https://developer.github.com/webhooks/

<h2>Repositories</h2>

<b>Jean-Pascal Evette (SVG with ECMAScript):</b> https://github.com/JeanPascalEvette/FBXToSVG

<b>Mircea Catana (SVG from Python):</b> https://github.com/mircea-catana/FBX_SVG

<b>Adam Joyce (SVG with ECMAScript):</b> https://github.com/adamjoyce/fbx-parser


