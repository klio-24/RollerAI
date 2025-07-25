'use client'; // Needed because we use client-side interactivity (useState, fetch)

import { useState,useEffect } from 'react'; // this is a React tool allowing functional components to have a state

export default function HomePage() { // This is the homepage stuff
  const [prompt, setPrompt] = useState(''); // tracks what the user typed into the text input
  const [status, setStatus] = useState(''); // tracks messages for the user
  const [jobID, setJobID] = useState(null);
  const [imageUrl, setImageUrl] = useState(null); // 'null' as we won't have the URL until image is rendered so will be null for a while
  // FOR ABOVE: useState needs two variable names - one is the variable, the other is the setter function which updates
  // the value and tells React to rerender the component

  const handleSubmit = async (e: React.FormEvent) => { // forms an asynchronous function (can use await key word)
    e.preventDefault(); // stops page reloaded when HTML form is submitted, 'e' is a common letter used to represent the event
    setStatus('Submitting...');
    setImageUrl(null);

    try { // here we have a try/catch clause
      const res = await fetch('https://vt6hi5a1th.execute-api.eu-west-2.amazonaws.com/generate', { // sends HTTP request to URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // tells server JSON data is being sent
        },
        body: JSON.stringify({ prompt }), // converts the text to JSON string
      });

      const data = await res.json(); // reads server's response

      setJobID(data.job_id)
      console.log("Received job ID from server:", data.job_id);
      setStatus(`Job ID: ${data.job_id}`);  // gives user the Job ID assigned by the backend 
    console.log("jobID after set:", data.job_id);
      // WE STILL use data.job_id as setJobID is asynchronous
    } catch (err) { // catch block
      setStatus("Error sending prompt");
      console.error(err);
    }
  };

  // After we've done the initial POST, we then wait for a response for the URL

useEffect(() => {
  if (!jobID) return; // If no job has been submitted, do nothing 

  console.log('Polling started for jobID:', jobID);
  setStatus('Image is being created...');

  // Wrap async logic inside a named function
  const poll = async () => {
    try {
      console.log("before await fetch");
      const res = await fetch(`https://vt6hi5a1th.execute-api.eu-west-2.amazonaws.com/status?job_id=${jobID}`);
      console.log("after await fetch");
      console.log("Fetch response:", res);
      
      const data = await res.json();
      console.log("Status result:", data.status);

      if (data.status == "complete") {
        console.log("inside if datastatus equals complete now");
        setImageUrl(data.s3_url);
        console.log("imageUrl state after set:", imageUrl);
        setStatus('Image ready!');
        clearInterval(interval);
      } else {
        console.log("else statement");
      }
    } catch (err) {
      console.error('Error polling job status', err);
    }
  };

  // Call the poll function on an interval
  const interval = setInterval(() => {
    console.log("interval tick");
    poll(); // properly call the async function
  }, 5000);

  return () => clearInterval(interval); // cleanup on unmount or jobID change
}, [jobID]);
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
      {imageUrl && ( // if imageUrl is non-null then render the following block
        <div>
          <h2>Generated Image:</h2>
          <img src={imageUrl} alt="Generated" style={{ maxWidth: '100%', marginTop: '1rem' }} /> 
        </div> // "Generated" provides alternative text if the image fails to load
      )}

    </div>
  );
}