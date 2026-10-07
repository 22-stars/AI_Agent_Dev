from state import *
state = create_state(
    "Generate a password and tell me the current time."
)

print("initial state")
print(state)

add_action(state, "generate_password")
record_observation(state, "generate_password", "password: 1234567890")
next_step(state)

print("\nState after one iteration")
print(state)

finish(state, "password: 123343\nCurrent Time: 10:35 AM")

print("\nFinal State")
print(state)