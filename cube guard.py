import anki_vector
from anki_vector.events import Events
from anki_vector.util import degrees
import threading
import time

said_text = False

def object_tapped(robot, event_type, event, evt):
    print("Vector sees a face")
    global said_text
    if not said_text:
        said_text = True
        robot.behavior.say_text("you have trigger a alarm!")
        robot.behavior.say_text(" you knocked mr cube ,please dont mess with him!")
        robot.audio.stream_wav_file('truck_reversing.wav')
        

        
        evt.set()


def object_moved(robot, event_type, event, evt):
    print("Vector sees a face")
    global said_text
    if not said_text:
        said_text = True
        robot.behavior.say_text("you have trigger a alarm!")
        robot.behavior.say_text(" you lifted the cube ,very light finger of you ,please dont mess with me!")
        robot.audio.stream_wav_file('truck_reversing.wav')


        
        evt.set()




with anki_vector.Robot(enable_face_detection=True) as robot:

    print ("Disconnecting from any connected cube...")
    robot.world.disconnect_cube()
    print("Going to wait for 3 seconds to shut off all connections")
    time.sleep(5)
    print("Woken up")

    connectionResult = robot.world.connect_cube()
    print (connectionResult)

    connected_cube = robot.world.connected_light_cube
    print (connected_cube)
    if connected_cube:
       print("Connected to cube {0}".format(connected_cube.factory_id))
       robot.world.flash_cube_lights()
    robot.behavior.set_head_angle(degrees(35.0))
    robot.behavior.set_lift_height(0.0)
    robot.behavior.say_text("mr cube is guarding this!")

    # If necessary, move Vector's Head and Lift to make it easy to see his face
    robot.behavior.set_head_angle(degrees(45.0))
    robot.behavior.set_lift_height(0.0)

    evt = threading.Event()
    robot.events.subscribe(object_tapped, Events.object_tapped, evt)
    robot.events.subscribe(object_moved, Events.object_moved, evt)

    print("Cube Guarding" )

    try:
        if not evt.wait(timeout=60000):
            print("------ Vector cube alarm off! ------")
    except KeyboardInterrupt:
        pass

robot.events.unsubscribe(on_robot_observed_face, Events.robot_observed_face)
