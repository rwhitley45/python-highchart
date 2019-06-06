__author__ = 'Ryan Whitley'

class Highchart:

    def __init__(self, x: 'List', y: 'List', chart_options: 'List'):
        if (len(x) != len(y) or
                (len(chart_options[5]) > 0 and len(chart_options[5]) != len(x)) or
                (len(chart_options[6]) > 0 and len(chart_options[6]) != len(x)) or
                (len(chart_options[8]) > 0 and len(chart_options[8]) != len(x))):
            raise ValueError("Length mismatch")

        assert (chart_options[1] == 'line' or chart_options[1] == 'scatter' or chart_options[1]
                == 'bar' or chart_options[1] == 'area' or chart_options[1] 
                == 'column'), "Please select either 'line', 'scatter', 'area', 'column' or 'bar' for plot type"

        if chart_options[9]:
            assert (chart_options[9] == 'polynomial' or chart_options[
                    9] == 'linear'), "Regression must either be '', 'polynomial', or 'linear'"

        self.x = x
        self.y = y
        self.title = chart_options[0]
        self.plot = chart_options[1]
        self.x_type = chart_options[2]
        self.cats = chart_options[3]
        self.y_title = chart_options[4]
        self.colors = chart_options[5]
        self.lgnd_titles = chart_options[6]
        self.div = chart_options[7]
        self.error = chart_options[8]
        self.regression = chart_options[9]

    def format_series(self, x, y, series_type, colors, name, error, regression) -> 'str':
        """ Returns (multiple) series as Highcharts Formatted String """
        series = ""
        if error:
            for i in range(len(error)):
                series += "{\n"
                series += "name: '" + name[i] + " error',\n"
                series += "type: 'errorbar',\n"
                series += "data: ["
                for j in range(len(error[i])):
                    if j != len(error[i]) - 1:
                        series += "[" + str(error[i][j][0]) + \
                            "," + str(error[i][j][1]) + "],"
                    else:
                        series += "[" + str(error[i][j][0]) + \
                            "," + str(error[i][j][1]) + "]]"

                series += "\n},"

        for i in range(len(x)):
            series += "{\n"
            series += "type: '" + series_type + "',\n"

            if regression:
                series += "regression: true,\n"
                series += "regressionSettings: {\n"
                series += 'name: "r2: %r",\n'
                series += "color: 'red',\n"
                series += "type: '" + regression + "'\n},\n"

            if colors:
                series += "color: '" + colors[i] + "',\n"
            if name:
                series += "name: '" + name[i] + "',\n"
            series += "data: ["
            for j in range(len(x[i])):
                if j != len(x[i]) - 1:
                    series += "[" + str(x[i][j]) + "," + str(y[i][j]) + "],"
                else:
                    series += "[" + str(x[i][j]) + "," + str(y[i][j]) + "]]"
            if i != len(x) - 1:
                series += "\n},"
            else:
                series += "\n}"
        return series

    def js_boiler(self):
        """ Highchart JS Boilerplate """
        return """
    $(function () {
            $('#%s').highcharts({
                    title: {
                            text:'%s'
                    },
                    xAxis: {
                            type: '%s',
                            categories: %s
                    },
                    yAxis: {
                            title: {
                                    text: '%s'
                            }
                    },
                    legend: {
                            enabled: true
                    },
                    scrollbar: {
                            enabled: true
                    },
                    series: [%s]
            });
    });
        """

    def get_imports(self):
        """ Imports for Jquery and Highcarts """
        return """
    <script
      src="https://code.jquery.com/jquery-3.3.1.min.js"
      integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
      crossorigin="anonymous"></script>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/highcharts-more.js"></script>
    <script src="https://code.highcharts.com/modules/data.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    <script src="../regression.js"> </script>
    <script src="https://code.highcharts.com/modules/broken-axis.js"></script>
        """

    def highcharts_str(self) -> 'str':
        boiler = self.js_boiler()
        hc_str = self.format_series(self.x, self.y, self.plot, self.colors,
                               self.lgnd_titles, self.error, self.regression)
        js_full = boiler % (self.div, self.title, self.x_type, self.cats, self.y_title,
                            hc_str)
        return js_full


def main():
    f = open("test_line.html", 'w')
    imports = get_imports()
    f.write(imports)
    f.write("\n<div id=\"container\"></div>\n")
    f.write("\n<script type=\"text/javascript\" charset=\"utf-8\">")
    x = [[1, 2, 3, 4, 5, 6, 8], [0, 1, 2]]
    y = [[5, 3, 2, 9, 10, 11, 13], [1, 8, -2]]
    cats = ['Hi', 'My', 'Name', 'Is', 'Ryan', 'Whitley']
    stderr = [[[5, 1], [10, 3], [3, 2], [8, 4], [
        6, 3], [4, 2]], [[9, 3.5], [7, 4.5], [10, 5]]]
    colors = ["red", "green"]
    legend_titles = ["Awesome", "Chart"]

    chart_options = ["Test Graph", 'bar', "category", cats,
                     "yaxis", colors, legend_titles, "container", stderr, 'linear']
    my_graph = Plot(x, y, chart_options)
    f.write(my_graph.highcharts_str())
    f.write("\n</script>")
    f.close()

if __name__ == '__main__':
    main()

