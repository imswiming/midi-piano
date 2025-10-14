import asyncio
import websockets
import mido

# --- List available MIDI outputs ---
outputs = mido.get_output_names()
print("Available MIDI outputs:")
for i, name in enumerate(outputs):
    print(f"{i}: {name}")

# --- Select output ---
while True:
    try:
        choice = int(input(f"Select MIDI output (0-{len(outputs)-1}): "))
        if 0 <= choice < len(outputs):
            midi_out = mido.open_output(outputs[choice])
            print(f"Using MIDI output: {outputs[choice]}")
            break
    except ValueError:
        pass
    print("Invalid choice. Try again.")

# --- WebSocket handler ---
async def handler(websocket):
    async for message in websocket:
        # Expect message as CSV: "status,data1,data2"
        try:
            status, data1, data2 = map(int, message.split(","))
            midi_out.send(mido.Message.from_bytes([status, data1, data2]))
        except Exception as e:
            print("Error parsing MIDI:", e)

# --- Main async server ---
async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket MIDI bridge running on ws://192.168.1.2:8765")
        await asyncio.Future()  # keep running forever

# --- Run server ---
asyncio.run(main())
