import asyncio
import websockets
import mido

# Change this to the MIDI output you want (your DAW or virtual port)
midi_out = mido.open_output(mido.get_output_names()[0])

async def handler(websocket):
    async for message in websocket:
        # Expect message as CSV: "status,data1,data2"
        try:
            status, data1, data2 = map(int, message.split(","))
            midi_out.send(mido.Message.from_bytes([status, data1, data2]))
        except Exception as e:
            print("Error parsing MIDI:", e)

start_server = websockets.serve(handler, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket MIDI bridge running on ws://192.168.1.2:8765")
asyncio.get_event_loop().run_forever()
