import subprocess

process = subprocess.Popen(['python', '-c 4', 'python.org'],
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

while True:
    output = process.stdout.readline()
    print(output.strip())
    # Do something else
    return_code = process.poll()
    if return_code is not None:
        print('RETURN CODE', return_code)
        # Process has finished, read rest of the output
        for output in process.stdout.readlines():
            print(output.strip())
        break

with open('test.csv', 'r') as f:
    line_count = 0
    line = f.readline()
    while line:
        if line_count == 5:
            break

        print(line)
        line = f.readline()

        line_count += 1
        break
    f.close()
    print('done')
