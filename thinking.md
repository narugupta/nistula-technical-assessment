# thinking.md — Part 3: Thinking Question

---

## Question A — The Immediate Response

**The AI message sent at 3am:**

> Hi Rahul, I'm really sorry — this should never have happened, especially with guests arriving in a few hours. Our caretaker has been woken up and is heading to Villa B1 right now — they'll be with you within 20 minutes. On the refund, you have my word we will make it right — our manager will call you personally in the morning. We're already moving.

**Why this wording:** At 3am a guest needs ownership, not process. The message gives a hard ETA to cut uncertainty, avoids promising a specific refund amount the AI has no authority to honour, and closes with momentum. The tone is human — because Nistula is not a call centre.

---

## Question B — The System Design

The moment the message is classified as `complaint`, normal AI auto-send is suspended. A human owns this now.

The system classifies the message as a complaint, immediately suspends auto-send for the thread, fires the AI reply, and alerts the caretaker and operations manager with the guest's exact words — not a summary. A full event timeline begins logging from this point.

**The 30-minute SLA timer starts at escalation creation, not when someone reads it.**

If no human acknowledges within 30 minutes: owner and backup manager receive a `SECOND NOTICE`, escalation priority upgrades, and the guest receives a holding message — *"Our team is on their way. Someone will reach you in 10 minutes."* The guest's experience during the silence is part of the incident. System keeps alerting until someone explicitly takes named ownership.

Everything logged: response time, resolution time, refund issued, final guest sentiment — feeding directly into pattern detection.

---

## Question C — The Learning

Three complaints in two months is an operational reliability failure. The system should have caught this after the second one.

**What I would build:** A Property Health Layer querying complaints nightly by `property_id` + `issue_category`. Two occurrences within 60 days auto-creates a maintenance ticket and flags the property. The flag stays open until an owner closes it with a resolution note — without a hard close condition, the ticket just sits there and nothing actually gets fixed.

A pre-stay caretaker checklist — hot water, WiFi, AC, power — must be completed before the property is marked guest-ready. Incomplete checklist blocks check-in.

And if an unresolved flag exists when a new guest arrives, the AI's escalation threshold for that property drops automatically. The third guest should never bear the cost of a problem we already knew about.