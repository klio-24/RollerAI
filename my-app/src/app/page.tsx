'use client'; // Needed because we use client-side interactivity (useState, fetch)

import { useState } from 'react'; // this is a React tool allowing functional components to have a state

export default function HomePage() { // This is the homepage stuff
  const [prompt, setPrompt] = useState(''); // tracks what the user typed into the text input
  const [status, setStatus] = useState(''); // tracks messages for the user

  const handleSubmit = async (e: React.FormEvent) => { // forms an asynchronous function (can use await key word)
    e.preventDefault(); // stops page reloaded when HTML form is submitted, 'e' is a common letter used to represent the event
    setStatus('Submitting...');

    try { // here we have a try/catch clause
      const res = await fetch('https://vt6hi5a1th.execute-api.eu-west-2.amazonaws.com/generate', { // sends HTTP request to URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // tells server JSON data is being sent
        },
        body: JSON.stringify({ prompt }), // converts the text to JSON string
      });

      const data = await res.json(); // reads server's response
      setStatus(`Job ID: ${data.job_id}`);  // gives user an job ID
    } catch (err) { // catch block
      setStatus('Error sending prompt');
      console.error(err);
    }
  };

  return ( // the actual functional components (textbox/button)
    <div style={{ padding: '2rem' }}>
      <h1>Generate Image</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter prompt"
          style={{ width: '300px', marginRight: '10px' }}
        />
        <button type="submit">Submit</button>
      </form>
      <p>{status}</p>
    </div>
  );
}