html = open('/dev/stdin').read()
with open('/home/user/Orlando-/index.html', 'w') as f:
    f.write(html)
print('written')
