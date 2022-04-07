import tkinter as tk
from typing import TYPE_CHECKING, List, Union

from Matrix import Matrix
from Point import Point
from Polygon import Polygon
from Vector import Vector

# Note: [Python] Scaled everything by a factor of 2 to feel more responsive
SCALE = 2

# Velocity vectors in pixels per second
X_VEL = Vector(int(500*SCALE), 0, 0)
Y_VEL = Vector(0, int(500*SCALE), 0)
Z_VEL = Vector(0, 0, int(500*SCALE))

FPS = 100

MOUSE_SENS_X = int(1000/SCALE)
MOUSE_SENS_Y = int(1500/SCALE)

# numPoints = 4
numPolygons = 2
polygons = [
    Polygon([
        Point(100, 100, 1000),
        Point(300, 100, 1000),
        Point(300, 300, 1000),
        Point(100, 300, 1000),
    ]),
]

angleX = angleY = 0.0

mouseX = mouseY = -1

windowWidth: int
windowHeight: int

def isInView(p: Union[Polygon, Point]) -> bool:
    if isinstance(p, Polygon):
        # true if all four of the polygon's points are in view
        for i in range(len(p.vertices)):
            if not isInView(p.vertices[i]):
                return False
        return True
    return (p.z >= 0 and abs(p.x) <= windowWidth + 2 * p.z
            and abs(p.y) <= windowHeight + 2 * p.z)

def main() -> None:
    global windowWidth, windowHeight

    # Create the window
    root = tk.Tk()

    # Set minimum and initial window sizes
    root.minsize(300, 200)
    root.geometry("400x250")

    # Create a canvas widget
    canvas = tk.Canvas(root, highlightthickness=0, background="white")
    canvas.pack(expand=True, fill="both")

    # Time between updates
    update_delay = 1000 // FPS

    # Update the window with new minsize and canvas
    root.update()

    # Initialize window size variables
    windowWidth = root.winfo_width()
    windowHeight = root.winfo_height()

    # Set up polygons
    for x in range(-1000, 1000, 200):
        polygons.append(
            Polygon([
                Point(x, 1000, -10000),
                Point(x+50, 1000, -10000),
                Point(x+50, 1000, 10000),
                Point(x, 1000, 10000),
            ])
        )
    numPolygons = len(polygons)

    # Key pressed states
    leftArrowKeyIsPressed = False
    rightArrowKeyIsPressed = False
    upArrowKeyIsPressed = False
    downArrowKeyIsPressed = False
    shiftIsPressed = False
    spaceIsPressed = False
    dx = dy = 0  # change in mouse position

    # Set the types of events we are interested in
    # - StructureNotifyMask: for when the window first appears on screen (MapNotify event)
    # - KeyPressMask: for getting keyboard pressed events (KeyPress)
    # - KeyReleaseMask: for getting keyboard released events (KeyRelease)
    # - PointerMotionMask: for getting mouse pointer movement events (MotionNotify)

    # Handle events

    # Python type annotations
    if TYPE_CHECKING:
        CanvasEvent = tk.Event[tk.Canvas]
        MiscEvent = tk.Event[tk.Misc]
    else:
        CanvasEvent = MiscEvent = tk.Event

    # Left click to "drag" the camera around
    def on_drag_down(xMotionEvent: CanvasEvent) -> None:
        global mouseX, mouseY
        mouseX = xMotionEvent.x
        mouseY = xMotionEvent.y
    def on_drag_move(xMotionEvent: CanvasEvent) -> None:
        global mouseX, mouseY
        nonlocal dx, dy
        dx -= xMotionEvent.x - mouseX  # negative
        dy -= xMotionEvent.y - mouseY  # negative
        mouseX = xMotionEvent.x
        mouseY = xMotionEvent.y
    canvas.bind("<ButtonPress-1>", on_drag_down)
    canvas.bind("<B1-Motion>", on_drag_move)

    # Right click to pan around
    def on_pan_down(xMotionEvent: CanvasEvent) -> None:
        global mouseX, mouseY
        mouseX = xMotionEvent.x
        mouseY = xMotionEvent.y
    def on_pan_move(xMotionEvent: CanvasEvent) -> None:
        global mouseX, mouseY
        nonlocal dx, dy
        dx += xMotionEvent.x - mouseX
        dy += xMotionEvent.y - mouseY
        mouseX = xMotionEvent.x
        mouseY = xMotionEvent.y
    canvas.bind("<ButtonPress-3>", on_pan_down)
    canvas.bind("<B3-Motion>", on_pan_move)

    def on_resize(xConfEvent: MiscEvent) -> None:
        global windowWidth, windowHeight
        # If window is resized, update local window size variables
        if xConfEvent.width != windowWidth:
            windowWidth = xConfEvent.width
        if xConfEvent.height != windowHeight:
            windowHeight = xConfEvent.height
    root.bind("<Configure>", on_resize)

    def on_key_press(event: MiscEvent) -> None:
        nonlocal \
            leftArrowKeyIsPressed, \
            rightArrowKeyIsPressed, \
            upArrowKeyIsPressed, \
            downArrowKeyIsPressed, \
            shiftIsPressed, \
            spaceIsPressed

        # Get the key symbol ("left", "up", etc.) of the KeyPress event
        keySymbol = event.keysym.lower()
        # Handle event depending on which key was pressed
        #
        # Set appropriate key state
        if keySymbol in (
            "a",
            "left",
        ):
            leftArrowKeyIsPressed = True
        elif keySymbol in (
            "d",
            "e",  # for dvorak layout
            "right",
        ):
            rightArrowKeyIsPressed = True
        elif keySymbol in (
            "w",
            ",",  # for dvorak layout
            "up",
        ):
            upArrowKeyIsPressed = True
        elif keySymbol in (
            "s",
            "o",  # for dvorak layout
            "down",
        ):
            downArrowKeyIsPressed = True
        elif keySymbol == "shift_l":
            shiftIsPressed = True
        elif keySymbol == "space":
            spaceIsPressed = True
        # If 'q' is pressed, exit
        elif keySymbol == "q":
            # Cleanup and exit
            #
            # Detroy the window
            root.destroy()
    root.bind("<KeyPress>", on_key_press)

    def on_key_release(event: MiscEvent) -> None:
        nonlocal \
            leftArrowKeyIsPressed, \
            rightArrowKeyIsPressed, \
            upArrowKeyIsPressed, \
            downArrowKeyIsPressed, \
            shiftIsPressed, \
            spaceIsPressed
        # Auto-repeated keypresses in tkinter don't emit a KeyRelease event
        # fortunately. (The original code has code that checks and ignores
        # these events.)
        #
        # Get the key symbol ("left", "up", etc.) of the KeyPress event
        keySymbol = event.keysym.lower()
        # Handle event depending on which key was released
        #
        # Unset appropriate key state
        if keySymbol in (
            "a",
            "left",
        ):
            leftArrowKeyIsPressed = False
        elif keySymbol in (
            "d",
            "e",  # for dvorak layout
            "right",
        ):
            rightArrowKeyIsPressed = False
        elif keySymbol in (
            "w",
            ",",  # for dvorak layout
            "up",
        ):
            upArrowKeyIsPressed = False
        elif keySymbol in (
            "s",
            "o",  # for dvorak layout
            "down",
        ):
            downArrowKeyIsPressed = False
        elif keySymbol == "shift_l":
            shiftIsPressed = False
        elif keySymbol == "space":
            spaceIsPressed = False
    root.bind("<KeyRelease>", on_key_release)

    # Game loop
    def on_update() -> None:
        global angleX, angleY
        nonlocal dx, dy

        # Update game state

        # Translate each polygons
        for i in range(numPolygons):
            if leftArrowKeyIsPressed:
                polygons[i] += Matrix.rotateY(X_VEL/FPS, -angleX)
            if rightArrowKeyIsPressed:
                polygons[i] -= Matrix.rotateY(X_VEL/FPS, -angleX)
            if upArrowKeyIsPressed:
                # Note: [Python] The commented out version doesn't work as
                # expected for some reason (and I'm too bad at math to
                # understand why).
                # polygons[i] -= Matrix.rotateX(Matrix.rotateY(Z_VEL/FPS, -angleX), angleY)
                polygons[i] -= Matrix.rotateY(Matrix.rotateX(Z_VEL/FPS, -angleY), -angleX)
            if downArrowKeyIsPressed:
                # polygons[i] += Matrix.rotateX(Matrix.rotateY(Z_VEL/FPS, -angleX), angleY)
                polygons[i] += Matrix.rotateY(Matrix.rotateX(Z_VEL/FPS, -angleY), -angleX)
            if spaceIsPressed:
                # Here we add because the positive y-axis is downward
                polygons[i] += Y_VEL/FPS
            if shiftIsPressed:
                # Here we subtract because the positive y-axis is downward
                polygons[i] -= Y_VEL/FPS

        # Set up polygons to draw
        transformedPolygons: List[Polygon] = [Polygon() for _ in range(numPolygons)]

        # Set up rotation angles
        angleX += -dx / MOUSE_SENS_X
        angleY += dy / MOUSE_SENS_Y

        # Rotate the polygons
        for i in range(numPolygons):
            # Here, Matrix.rotateY() rotates about the y-axis.
            # Hence, angleX is passed to rotateY() (up-down view rotation).
            # Similarly, angleY is passed to rotateX() (left-right view rotation)
            transformedPolygons[i] = Matrix.rotateY(polygons[i], angleX)
            transformedPolygons[i] = Matrix.rotateX(transformedPolygons[i], angleY)

        # Clip points to boundary of the viewing frustum
        for i in range(numPolygons):
            currPoly = transformedPolygons[i]

            # If one or more of the vertices are out of view,
            # clip the polygon to the viewing frustum
            if not isInView(currPoly):

                # All vertices of newPoly will be in the viewing frustum
                newPoly = Polygon()

                # Number of vertices of the current polygon
                numVertices = len(currPoly.vertices)

                # Loop over the current polgon's vertices
                for j in range(numVertices):
                    currPoint = transformedPolygons[i].vertices[j]
                    nextPoint = transformedPolygons[i].vertices[(j+1) % numVertices]

                    if isInView(currPoint):
                        newPoly.vertices.append(currPoint)

                    # If the points lie across the border of the viewing frustum
                    if isInView(currPoint) ^ isInView(nextPoint):
                        if isInView(currPoint):
                            inView, outOfView = currPoint, nextPoint
                        else:
                            inView, outOfView = nextPoint, currPoint

                        # Locate the intersection of the line connecting
                        # inView and outView with the boundary of the
                        # viewing frustum
                        while True:
                            midpoint = Point.getMidpoint(inView, outOfView)
                            if midpoint == inView or midpoint == outOfView:
                                break
                            elif isInView(midpoint):
                                inView = midpoint
                            else:
                                outOfView = midpoint
                        intersectionPoint = inView

                        # Add the intersectionPoint (which is in view) to the new polygon
                        newPoly.vertices.append(intersectionPoint)

                # Replace current polygon with clipped polygon
                transformedPolygons[i] = newPoly

        for i in range(numPolygons):
            for j in range(len(transformedPolygons[i].vertices)):
                pass
                # p = transformedPolygons[i].vertices[j]
                # print("Polygon %d, Vertex %d: (%d,%d,%d)" % (i, j, p.x, p.y, p.z))

        # Clear the window
        canvas.delete("all")

        # Project the polygons onto the viewing plane
        for i in range(numPolygons):
            numVertices = len(transformedPolygons[i].vertices)

            # Note: [Python] Don't draw if there's no point (haha pun :P)
            # because otherwise tkinter complains about an empty list.
            if not numVertices:
                continue

            xPoints = [[0.0, 0.0] for _ in range(numVertices)]
            for j in range(numVertices):
                xPoints[j][0] = transformedPolygons[i].vertices[j].x
                xPoints[j][1] = transformedPolygons[i].vertices[j].y

                # If the point is in view, scale it
                # if isInView(transformedPolygons[i].vertices[j]):
                if True:
                    # Scale the point according to how far away from the viewing plane it is (z coordinate)
                    xPoints[j][0] = transformedPolygons[i].vertices[j].x * windowWidth / (windowWidth + 2 * transformedPolygons[i].vertices[j].z)
                    xPoints[j][1] = transformedPolygons[i].vertices[j].y * windowHeight / (windowHeight + 2 * transformedPolygons[i].vertices[j].z)

                # Translate from game coordinates to screen coordinates
                xPoints[j][0] = xPoints[j][0] + windowWidth / 2
                xPoints[j][1] = xPoints[j][1] + windowHeight / 2

            # Fill in a polygon connecting each of the points
            canvas.create_polygon(
                *xPoints,
                # Set of reusable drawing parameters
                # Note: [Python] width is 0 to minimize canvas artifacts left over from
                # redrawing. https://stackoverflow.com/a/54203448
                width=0,
                fill="black",
                outline="",
            )

        # Reset rotation variables
        dx = dy = 0

        # Pause for a bit
        canvas.after(update_delay, on_update)

    # Start the update loop
    canvas.after_idle(on_update)

    # Run event loop until root is destroyed
    root.mainloop()

if __name__ == "__main__":
    main()
