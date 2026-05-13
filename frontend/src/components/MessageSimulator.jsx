import { useState } from "react";

import axios from "axios";


export default function MessageSimulator() {

  const [guestName, setGuestName] =
    useState("");

  const [message, setMessage] =
    useState("");

  const [source, setSource] =
    useState("whatsapp");

  const [response, setResponse] =
    useState(null);

  const [loading, setLoading] =
    useState(false);


  async function sendMessage() {

    setLoading(true);

    try {

      const payload = {
        source,
        guest_name: guestName,
        message,
        timestamp: new Date().toISOString(),
        booking_ref: "NIS-DEMO",
        property_id: "villa-b1"
      };

      const res = await axios.post(
        "http://localhost:8000/webhook/message",
        payload
      );

      // backend only acknowledges async processing
      // so frontend simulates operational visibility
      setResponse(res.data);

    } catch (err) {

      console.error(err);

      setResponse({
        error: "Request failed"
      });

    } finally {

      setLoading(false);
    }
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
        Guest Message Simulator
      </h2>

      <input
        placeholder="Guest Name"
        value={guestName}
        onChange={(e) =>
          setGuestName(e.target.value)
        }

        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px"
        }}
      />

      <select
        value={source}
        onChange={(e) =>
          setSource(e.target.value)
        }

        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px"
        }}
      >

        <option value="whatsapp">
          WhatsApp
        </option>

        <option value="instagram">
          Instagram
        </option>

        <option value="booking_com">
          Booking.com
        </option>

      </select>

      <textarea
        placeholder="Guest Message"
        value={message}

        onChange={(e) =>
          setMessage(e.target.value)
        }

        rows={5}

        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px"
        }}
      />

      <button
        onClick={sendMessage}
        disabled={loading}

        style={{
          padding: "10px 20px",
          cursor: "pointer"
        }}
      >

        {
          loading
            ? "Sending..."
            : "Send Message"
        }

      </button>

      {
  response && (

    <div
      style={{
        marginTop: "20px",
        background: "#fafafa",
        padding: "15px",
        borderRadius: "10px"
      }}
    >

      <h3>
        AI Response
      </h3>

      {
        response.error ? (

          <p>
            {response.error}
          </p>

        ) : (

          <div>

            <p>
              <strong>
                Reply:
              </strong>
            </p>

            <p>
              {response.drafted_reply}
            </p>

            <p>
              <strong>
                Action:
              </strong>
              {" "}
              {response.action}
            </p>

            <p>
              <strong>
                Confidence:
              </strong>
              {" "}
              {response.confidence_score}
            </p>

            <p>
              <strong>
                Query Type:
              </strong>
              {" "}
              {response.query_type}
            </p>

          </div>
        )
      }

    </div>
  )
}

    </div>
  );
}