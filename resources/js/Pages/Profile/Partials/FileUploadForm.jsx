import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FileUploadForm = ({ fetchUserFiles }) => {
    const [file, setFile] = useState(null);

    const handleSubmit = (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('pdf', file);

        axios.post('/file/upload', formData)
            .then(response => {
                console.log(response);
                fetchUserFiles();
            })
            .catch(error => {
                console.error(error);
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
