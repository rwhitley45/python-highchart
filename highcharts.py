__author__ = 'Ryan Whitley'


class Highchart:
    """ Class for converting data to be plotted into boilerplate highcharts javascript code """

    def __init__(self, x: 'List', y: 'List', chart_options=['', 'scatter', 'category', [], '', [], [], 'container', [], '']):
        """ Init method for the class

            Args:
                x: 2D Array Containing x-coordinate information
                y: 2D Array Containing y-coordinate information
                chart_options: Array containing chart information as follows:
                    chart_options[0](str): Chart Title (optional blank)
                    chart_options[1](str): Type of Plot
                    chart_options[2](str): X-Axis Type(category, datetime, etc..)
                    chart_options[3](List[str]): Categories Array (optional blank)
                    chart_options[4](str): Y-Axis Title (optional blank)
                    chart_options[5](List[str]): Array representing colors of different series (optional blank)
                    chart_options[6](List[str]): Array of series titles
                    chart_options[7](str): div name (for embedding)
                    chart_options[8](List[ List[high,low] ]): Standard Deviations (optional blank)
                    chart_options[9](str): Perform linear or polnomial regression (optional blank)

        """
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
        self.name = chart_options[6]
        self.div = chart_options[7]
        self.error = chart_options[8]
        self.regression = chart_options[9]

    def format_series(self) -> 'str':
        """ Returns (multiple) series as Highcharts Formatted String 

            Note:
                Maintaining consistency accross the data is important here
        """
        series = ""
        if self.error:
            for i in range(len(self.error)):
                series += "{\n"
                series += "name: '" + self.name[i] + " error',\n"
                series += "type: 'errorbar',\n"
                series += "data: ["
                for j in range(len(self.error[i])):
                    if j != len(self.error[i]) - 1:
                        series += "[" + str(self.error[i][j][0]) + \
                            "," + str(self.error[i][j][1]) + "],"
                    else:
                        series += "[" + str(self.error[i][j][0]) + \
                            "," + str(self.error[i][j][1]) + "]]"

                series += "\n},"

        for i in range(len(self.x)):
            series += "{\n"
            series += "type: '" + self.plot + "',\n"

            if self.regression:
                series += "regression: true,\n"
                series += "regressionSettings: {\n"
                series += 'name: "r2: %r",\n'
                series += "color: 'red',\n"
                series += "type: '" + self.regression + "'\n},\n"

            if self.colors:
                series += "color: '" + self.colors[i] + "',\n"
            if self.name:
                series += "name: '" + self.name[i] + "',\n"
            series += "data: ["
            for j in range(len(self.x[i])):
                if j != len(self.x[i]) - 1:
                    series += "[" + str(self.x[i][j]) + \
                        "," + str(self.y[i][j]) + "],"
                else:
                    series += "[" + str(self.x[i][j]) + \
                        "," + str(self.y[i][j]) + "]]"
            if i != len(self.x) - 1:
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
        """ Imports for Jquery and Highcarts+plugins """
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
        """ returns full JavaScript coded string for embedding """
        boiler = self.js_boiler()
        hc_str = self.format_series()
        js_full = boiler % (self.div, self.title, self.x_type, self.cats, self.y_title,
                            hc_str)
        return js_full
