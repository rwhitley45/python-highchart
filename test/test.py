import sys
sys.path.append('../')

from highcharts import *

import pandas as pd


def main():
    df = pd.read_csv('data.csv')
    data = ['Nationality', 'Overall', 'Potential']
    data = df[data]
    averages = dict()

    for i in data.index:
        if data['Nationality'][i] in averages:
            averages[data['Nationality'][i]][0].append(data['Overall'][i])
            averages[data['Nationality'][i]][1].append(data['Potential'][i])
        else:
            averages[data['Nationality'][i]] = [
                [data['Overall'][i]], [data['Potential'][i]]]

    for key in averages.keys():
        size_overall = len(averages[key][0])
        mean_overall = sum(averages[key][0]) / size_overall
        averages[key][0] = mean_overall

        size_potential = len(averages[key][1])
        mean_potential = sum(averages[key][1]) / size_potential
        averages[key][1] = mean_potential

    cats = list(averages.keys())
    x = range(0, len(cats))
    y_overall = []
    y_potential = []
    for val in averages.values():
        y_overall.append(val[0])
        y_potential.append(val[1])
    chart_options = ["Average Player Score By Country(FIFA)", 'column', 'category', cats, 'Average Score', [
    ], ['Overall', 'Potential'], "container", [], '']
    chart = Highchart([x, x], [y_overall, y_potential], chart_options)
    f = open("fifa.html", 'w')
    f.write(chart.get_imports())
    f.write("\n<div id=\"container\"></div>\n")
    f.write("\n<script type=\"text/javascript\" charset=\"utf-8\">")
    f.write(chart.highcharts_str())
    f.write("\n</script>")

    # scatter plot age/overall

    data = ['Age', 'Overall']
    data = df[data]
    x = []
    y = []
    for i in data.index:
        x.append(data['Overall'][i])
        y.append(data['Age'][i])

    chart_options = ["Age vs Overall Rank", 'scatter', 'category',
                     [], 'Age', [], ['Overall'], "container2", [], 'linear']
    chart = Highchart([x], [y], chart_options)
    f.write("\n<div id=\"container2\"></div>\n")
    f.write("\n<script type=\"text/javascript\" charset=\"utf-8\">")
    f.write(chart.highcharts_str())
    f.write("\n</script>")

    f.close()

if __name__ == '__main__':
    main()
