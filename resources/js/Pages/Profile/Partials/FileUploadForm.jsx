import React, { useState } from 'react';
import axios from 'axios';

const FileUploadForm = () => {
    const [file, setFile] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('pdf', file);
      
    axios.post('/file/upload', formData)
        .then(response => {
            console.log(response.data);
            // Redirect or show a success message
        })
        .catch(error => {
            console.error(error.response.data);
            // Handle errors
        });
    };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button type="submit">Upload</button>
    </form>
  );
};

export default FileUploadForm;
