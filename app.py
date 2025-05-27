from flask import Flask, render_template, request

app = Flask(__name__)

def findInterval(in_hour, in_min, out_hour, out_min):
    return (out_hour - (in_hour+1)) * 60 + (60 - in_min) + out_min

def Timer(mrng_time, am_checkout, am_checkin):
    mrng_hour = int(mrng_time.split(':')[0])
    mrng_min = int(mrng_time.split(':')[1])
    am_hour_out = int(am_checkout.split(':')[0])
    am_min_out = int(am_checkout.split(':')[1])
    am_hour_in = int(am_checkin.split(':')[0])
    am_min_in = int(am_checkin.split(':')[1])

    mrng_half_time = findInterval(mrng_hour, mrng_min, am_hour_out, am_min_out)
    free_time = findInterval(am_hour_out, am_min_out, am_hour_in, am_min_in)

    tot_time = 8 * 60
    rem_time = tot_time - mrng_half_time
    rem_time_hr = int(rem_time / 60)
    rem_time_min = rem_time % 60

    out_hour = am_hour_in + rem_time_hr
    out_min = am_min_in + rem_time_min + 10
    if out_min >= 60:
        out_min -= 60
        out_hour += 1
    # print(int(mrng_half_time/60), mrng_half_time%60, int(free_time/60), free_time%60, rem_time_hr, rem_time_min)
    return f"{out_hour}:{out_min:02d}"

# print(Timer("9:58", "13:24", "13:55"))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        mrng_time = request.form['mrng_time']
        am_checkout = request.form['am_checkout']
        am_checkin = request.form['am_checkin']
        result = Timer(mrng_time, am_checkout, am_checkin)
        return render_template('index.html', result=result)
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
