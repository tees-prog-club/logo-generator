import copy
import sys

class Point:
    """Represents a point on a 2D plane.

    """

    def __init__(self, x, y):
        """Initialises a new instance of a point on a 2D plane.

        Args:
            x (float): The x-coordinate of the point.
            y (float): The y-coordinate of the point.

        """
        self.x = float(x)
        self.y = float(y)

    def stringify(self):
        """Converts this point to its string representation.

        """
        return '{' + str(self.x) + ', ' + str(self.y) + '}'

def get_file_text(path):
    """Gets the text from the file at the specified path.

    Args:
        path (str): The path of the file to read.

    """
    with open(path, 'r') as file:
        data = file.read()
    return data

def set_file_text(path, text):
    """Sets the text in the file at the specified path.

    Args:
        path (str): The path of the file to write.
        text (str): The text to write to the file.

    """
    with open(path, "w") as file:
        file.write(text)

def load_colours(path):
    """Reads a list of colours from the file at the specified path.

    Args:
        path (str): The path of the file to read.

    """
    raw = get_file_text('colours.txt').replace('\r', '')
    lines = raw.split('\n')
    return lines
        
def load_vertices(path):
    """Reads a list of vertices from the file at the specified path.

    Args:
        path (str): The path of the file to read.

    """
    # Read file, normalising line endings.
    raw = get_file_text(path).replace('\r', '')
    lines = raw.split('\n') # Split into lines.
    vertices = [] # List of vertices.
    for line in lines:
        coordinates = line.split(',') # Split coordinate pair.
        # If we have a valid coordinate pair, add it to vertex list.
        if len(coordinates) == 2:
            vertices.append(Point(coordinates[0], coordinates[1]))
    return vertices

def is_closed(vertices):
    """Gets whether or not a vertex list forms a closed polygon.

    Args:
        vertices (Point[]): The vertex list to check.

    """
    # If first member is identical to last member, we have a closed polygon.
    return vertices[0].x == vertices[0].y and vertices[-1].x == vertices[-1].y

def close_verts(vertices):
    """Closes a polygon given as a set of vertices, if not closed already.

    Args:
        vertices (Point[]): The vertex list to check.

    """
    output = copy.deepcopy(vertices) # Don't modify original list.
    if is_closed(output):
        # Append new point identical to first member.
        output.append(copy.deepcopy(output[0]))
    return output

def translate_verts(vertices, x, y):
    """Translates a list of vertices by an offset.

    Args:
        vertices (Point[]): The vertex list to translate.
        x (Point[]):        The x-offset to translate by.
        y (Point[]):        The y-offset to translate by.

    """
    output = copy.deepcopy(vertices) # Don't modify original list.
    for node in output:
        node.x += x
        node.y += y
    return output

def sutherland_hodgman(subject, clip):
    """Applies Sutherland-Hodgman clipping to two polygons.
    
    Adapted from Rosetta Code Python example:
    https://rosettacode.org/wiki/Sutherland-Hodgman_polygon_clipping

    Args:
        subject (Point[]): The subject polygon.
        clip (Point[]):    The clipping polygon.

    """
    def inside(p, cp1, cp2):
        """Returns whether or not a point is inside the current clip edge.

        Args:
            p (Point):   The point to check.
            cp1 (Point): The first vertex of the clip edge.
            cp2 (Point): The second vertex of the clip edge.

        """
        return (cp2.x - cp1.x) * (p.y - cp1.y) > (cp2.y - cp1.y) * (p.x - cp1.x)

    def intersect(p1, p2, cp1, cp2):
        """Returns the intersection point of the given subject and clip edges.

        Args:
            p1 (Point):  The first vertex of the subject edge.
            p2 (Point):  The second vertex of the subject edge.
            cp1 (Point): The first vertex of the clip edge.
            cp2 (Point): The second vertex of the clip edge.

        """
        dc = Point(cp1.x - cp2.x, cp1.y - cp2.y)
        dp = Point(p1.x - p2.x, p1.y - p2.y)
        n1 = cp1.x * cp2.y - cp1.y * cp2.x
        n2 = p1.x * p2.y - p1.y * p2.x
        n3 = 1.0 / (dc.x * dp.y - dc.y * dp.x)
        return Point((n1 * dp.x - n2 * dc.x) * n3, (n1 * dp.y - n2 * dc.y) * n3)

    output = copy.deepcopy(subject) # Don't modify original list.
    
    cp1 = clip[-1] # Start with last vertex in clip polygon.
    for clip_vertex in clip:
        cp2 = clip_vertex
        inputList = output
        output = []
        s = inputList[-1] # Previous vertex.
        for subjectVertex in inputList:
            e = subjectVertex
            if inside(e, cp1, cp2): # First point is inside.
                if not inside(s, cp1, cp2): # Second point not inside.
                   output.append(intersect(s, e, cp1, cp2)) # Add intersection.
                output.append(e) # Add first point.
            elif inside(s, cp1, cp2): # Second point is inside, not first.
                output.append(intersect(s, e, cp1, cp2)) # Add intersection.
            s = e # Remember this subject vertex for next edge.
        cp1 = cp2 # Remember this clip vertex for next edge.
    return output

def svg_path(nodes, id, colour):
    """Returns an SVG path element for the nodes specified.

    Args:
        nodes (Point[]): The nodes of the path to create.
        id (str):        The ID of the path to create.
        colour (str):    The fill colour of the path to create.

    """
    element = "<g id=\"group_" + id + "\"><path id=\"" + id + "\" d=\"M "
    for node in nodes:
        element += str(node.x) + "," + str(node.y) + " "
    element += "Z\" style=\"fill:" + colour + ";fill-opacity:1\" /></g>"
    return element

# Load and close base shape.
subject = close_verts(load_vertices('base.poly'))

# Load and close clip shape.
base_clip = close_verts(load_vertices('clip.poly'))
    
# Load colours.
colours = load_colours('colours.txt')

# Initialize output as base shape with first colour.
paths = svg_path(subject, "base", colours[0])

# Add stripes.
stripes = int(sys.argv[1])
height = float(sys.argv[2])
for i in range(stripes):
    clip = translate_verts(base_clip, 0, i * height) # Translate clip shape.
    subpath = sutherland_hodgman(subject, clip) # Perform clipping
    colour = colours[(i + 1) % len(colours)] # Select stripe colour.
    paths += svg_path(subpath, "path_" + str(i), colour) # Add to output.

outline = get_file_text('outline.svg') # Get SVG template.
image = outline.replace('<!--%PATHS%-->', paths) # Replace placeholder.

# Write SVG to output.
set_file_text('logo.svg', image)
