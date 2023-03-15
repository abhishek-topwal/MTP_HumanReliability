import pylsl
f = open('pulse_data.txt', 'w')
f.seek(0)
f.truncate()

def pulse_stream():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    # use name of the stream to resolve it
    stream_pulse = pylsl.resolve_stream('name', 'obci_eeg2')

    # create a new inlet to read from the stream
    inlet_pulse = pylsl.StreamInlet(stream_pulse[0], processing_flags=pylsl.proc_ALL)

    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        chunk_pulse, timestamps_pulse = inlet_pulse.pull_sample()
        f.write("Pulse ||"+str(timestamps_pulse) + '||' + str(chunk_pulse)+'\n')

pulse_stream()