from flask import Flask, render_template, request

app = Flask(__name__)

train_timings = ["16:12", "16:42", "17:12", "17:42", "18:02", "18:22", "18:42", "19:02", "19:22", "19:42", "20:02", "20:22", "20:42", "21:02", "21:27", "21:52", "22:27", "22:57"]

def findInterval(in_hour, in_min, out_hour, out_min):
    return (out_hour - (in_hour+1)) * 60 + (60 - in_min) + out_min


def findTrain(mrng_time, am_checkout, am_checkin, break_mins = 0):
    result = Timer(mrng_time, am_checkout, am_checkin, break_mins)
    result_hr = int(result.split(':')[0])
    result_min = int(result.split(':')[1])
    mini = 24*60
    min_ind = -1
    for i in range(len(train_timings)): 
        train_hr = int(train_timings[i].split(':')[0])
        train_min = int(train_timings[i].split(':')[1])
        if (train_hr == result_hr and train_min >= result_min) or (train_hr > result_hr):
            res = abs(findInterval(result_hr, result_min, train_hr, train_min))
            if res >= mini:
                break
            else:
                mini = res
                min_ind = i
    return [result, min_ind]       

def Timer(mrng_time, am_checkout, am_checkin, break_mins):

    mrng_hour = int(mrng_time.split(':')[0])
    mrng_min = int(mrng_time.split(':')[1])
    am_hour_out = int(am_checkout.split(':')[0])
    am_min_out = int(am_checkout.split(':')[1])
    am_hour_in = int(am_checkin.split(':')[0])
    am_min_in = int(am_checkin.split(':')[1])

    mrng_half_time = findInterval(mrng_hour, mrng_min, am_hour_out, am_min_out)
    # free_time = findInterval(am_hour_out, am_min_out, am_hour_in, am_min_in)

    tot_time = 8 * 60
    rem_time = tot_time - mrng_half_time
    rem_time_hr = int(rem_time / 60)
    rem_time_min = rem_time % 60

    out_hour = am_hour_in + rem_time_hr
    out_min = am_min_in + rem_time_min + break_mins + 10
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
        break_mins = request.form['break_mins']
        break_mins = 0 if break_mins == '' else int(break_mins)
        result = findTrain(mrng_time, am_checkout, am_checkin, break_mins)
        out_time = result[0]
        next_train = result[1]
        return render_template('index.html', result=True,out_time= out_time, next_train=train_timings[next_train], trains_list = train_timings[next_train:min(next_train+3, len(train_timings))])
    return render_template('index.html', result=False)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

