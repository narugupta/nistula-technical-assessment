import MessageSimulator from "./components/MessageSimulator";
import EscalationTable from "./components/EscalationTable";
import MetricsPanel from "./components/MetricsPanel";

export default function App() {

  return (
    <div
      style={{
        fontFamily: "Arial",
        padding: "30px",
        background: "#f4f4f4",
        minHeight: "100vh"
      }}
    >

      <h1>
        Nistula Operations Playground
      </h1>

      <p>
        AI-assisted hospitality workflow simulator
      </p>

      <MessageSimulator />

      <EscalationTable />

      <MetricsPanel />

    </div>
  );
}