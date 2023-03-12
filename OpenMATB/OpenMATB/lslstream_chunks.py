import pylsl


f = open('data.txt', 'w')
f.seek(0)
f.truncate()

def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")

    # use name of the stream to resolve it
    stream_eeg = pylsl.resolve_stream('name', 'obci_eeg1')
    stream_pulse = pylsl.resolve_stream('name', 'obci_eeg2')

    # create a new inlet to read from the stream
    inlet_eeg = pylsl.StreamInlet(stream_eeg[0])
    inlet_pulse = pylsl.StreamInlet(stream_pulse[0], processing_flags=pylsl.proc_ALL)

    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        # offset = inlet_pulse.time_correction()
        # print(offset)
        chunk_eeg, timestamps_eeg = inlet_eeg.pull_sample()
        chunk_pulse, timestamps_pulse = inlet_pulse.pull_sample()
        # if timestamps_eeg:
        #     f.write("EEG ||"+str(timestamps_eeg) + '||' + str(chunk_eeg)+'\n')
            # print(timestamps, chunk)
        f.write("Pulse ||"+str(timestamps_pulse) + '||' + str(chunk_pulse)+'\n')

        # if timestamps_pulse:
        #     f.write("Pulse ||"+str(timestamps_pulse) + '||' + str(chunk_pulse)+'\n')


if __name__ == '__main__':
    main()