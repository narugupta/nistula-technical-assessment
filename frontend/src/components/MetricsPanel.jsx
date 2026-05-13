import { useEffect, useState } from "react";

import axios from "axios";


export default function MetricsPanel() {

  const [metrics, setMetrics] =
    useState(null);


  async function loadMetrics() {

    try {

      const res = await axios.get(
        "http://localhost:8000/operations/metrics"
      );

      setMetrics(res.data);

    } catch (err) {

      console.error(err);
    }
  }


  useEffect(() => {

    loadMetrics();

    // polling is enough for demo scale
    const interval = setInterval(
      loadMetrics,
      5000
    );

    return () =>
      clearInterval(interval);

  }, []);


  if (!metrics) {

    return (

      <div
        style={{
          background: "white",
          padding: "20px",
          marginTop: "20px",
          borderRadius: "10px"
        }}
      >

        Loading metrics...

      </div>
    );
  }


  return (

    <div
      style={{
        background: "white",
        padding: "20px",
        marginTop: "20px",
        borderRadius: "10px"
      }}
    >

      <h2>
        System Metrics
      </h2>

      <ul>

        <li>
          Total Messages:
          {" "}
          {metrics.total_messages}
        </li>

        <li>
          Total Escalations:
          {" "}
          {metrics.total_escalations}
        </li>

        <li>
          Failed Events:
          {" "}
          {metrics.failed_events}
        </li>

        <li>
          Auto Sends:
          {" "}
          {metrics.auto_send_count}
        </li>

      </ul>

    </div>
  );
}