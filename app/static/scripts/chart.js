fetch("/data")
    .then((response) => response.json())
    .then((data) => {
        const barCtx = document.getElementById("barChart").getContext("2d");
        const lineCtx = document.getElementById("lineChart").getContext("2d");

        new Chart(barCtx, {
            type: "bar",
            data: data.bar,
        });

        new Chart(lineCtx, {
            type: "line",
            data: data.line,
        });
    });
