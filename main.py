import classes
import events
import global_vars

player = classes.Player([global_vars.dimensions[0],global_vars.dimensions[1]],global_vars.PLAYER_HP,global_vars.PLAYER_HP,)
eventHandler = events.EventHandler()

while True:
