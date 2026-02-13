document.addEventListener("DOMContentLoaded", function () {

  function getSentimentData(canvas) {
    return {
      positive: parseInt(canvas.dataset.positive),
      neutral: parseInt(canvas.dataset.neutral),
      negative: parseInt(canvas.dataset.negative)
    };
  }

  /* ======================
     BAR CHART
  ====================== */
  const barCanvas = document.getElementById("sentimentChart");

  if (barCanvas) {
    const { positive, neutral, negative } = getSentimentData(barCanvas);

    new Chart(barCanvas, {
      type: "bar",
      data: {
        labels: ["Positive", "Neutral", "Negative"],
        datasets: [{
          label: "Number of Comments",
          data: [positive, neutral, negative],
          backgroundColor: [
            "rgba(34, 197, 94, 0.7)",
            "rgba(250, 204, 21, 0.7)",
            "rgba(239, 68, 68, 0.7)"
          ],
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }

  /* ======================
     DONUT CHART
  ====================== */
  const donutCanvas = document.getElementById("sentimentDonut");

  if (donutCanvas) {
    const { positive, neutral, negative } = getSentimentData(donutCanvas);

    new Chart(donutCanvas, {
      type: "doughnut",
      data: {
        labels: ["Positive", "Neutral", "Negative"],
        datasets: [{
          data: [positive, neutral, negative],
          backgroundColor: [
            "#22c55e",
            "#facc15",
            "#ef4444"
          ],
          borderWidth: 0
        }]
      },
      options: {
        cutout: "70%",
        responsive: true,
        plugins: {
          legend: {
            position: "bottom"
          }
        }
      }
    });
  }

});
