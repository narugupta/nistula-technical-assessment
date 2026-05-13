import { useEffect, useState } from "react";

import axios from "axios";


export default function EscalationTable() {

  const [escalations, setEscalations] =
    useState([]);


  async function loadEscalations() {

    try {

      const res = await axios.get(
        "http://localhost:8000/operations/escalations"
      );

      setEscalations(res.data);

    } catch (err) {

      console.error(err);
    }
  }


  useEffect(() => {

    loadEscalations();

    // lightweight polling for demo purposes
    const interval = setInterval(
      loadEscalations,
      15000
    );

    return () =>
      clearInterval(interval);

  }, []);


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
        Escalations
      </h2>

      <table
        width="100%"
        border="1"
        cellPadding="10"
      >

        <thead>

          <tr>
            <th>ID</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Agent</th>
          </tr>

        </thead>

        <tbody>

          {
            escalations.map((e) => (

              <tr key={e.id}>

                <td>{e.id}</td>

                <td>{e.severity}</td>

                <td>{e.status}</td>

                <td>
                  {e.assigned_agent_id}
                </td>

              </tr>
            ))
          }

        </tbody>

      </table>

    </div>
  );
}