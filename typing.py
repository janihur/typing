import sys
from blessed import Terminal
from time import perf_counter
from time import sleep

with open(sys.argv[1], 'r') as file:
    lines = [line.rstrip() for line in file]
    text = ' '.join(lines)

term = Terminal()

time = None
success_keys = 0
mistake_keys = 0

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    width = term.width
    start = 0
    end = len(text)
    visible_text = text[start:(start+width)]
    print(term.move_yx(0, 0) + term.clear_eol + visible_text)

    start_time = None
    i = 0
    while True:
        key = term.inkey()
        if start_time is None:
            start_time = perf_counter()
        if key.name == "KEY_ENTER":
            break
        if key == visible_text[i]:
            success_keys += 1
            if key == ' ':
                start += i
                start += 1
                visible_text = text[start:(start+width)]
                print(term.move_yx(0, 0) + term.clear_eol) 
                print(term.move_yx(0, 0) + visible_text)
                i = 0
            else:
                print(term.move_yx(0, i) + term.bold_green(visible_text[i]), end='', flush=True)
                i += 1
        else:
            mistake_keys += 1
            print(term.move_yx(0, i) + term.bold_red(visible_text[i]), end='', flush=True)

    time = perf_counter() - start_time

print(f'time: {time:.2f}s')
print(f'success_keys: {success_keys}')
print(f'mistake_keys: {mistake_keys}')
print(f'cpm: {(60/time*success_keys):.2f}')
print(f'error rate: {(mistake_keys/success_keys*100):.2f}%')
