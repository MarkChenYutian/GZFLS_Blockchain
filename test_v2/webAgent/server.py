from flask import Flask, request

app = Flask("sever")


@app.route('/', methods=['POST'])
def print_json():
    print(request.json)
    return "0"


if __name__ == '__main__':
    app.run()
