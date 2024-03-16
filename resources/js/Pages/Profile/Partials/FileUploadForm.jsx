import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FileUploadForm = ({ fetchUserFiles }) => {

    const [isLoading, setIsLoading] = useState(false);

    const [notice, setNotice] = useState("");

    const [file, setFile] = useState(null);

    const handleSubmit = (e) => {
        e.preventDefault();

        setIsLoading(true);

        setNotice("");

        const formData = new FormData();
        formData.append('file', file);

        axios.post('/file/upload_and_ingest', formData)
            .then(response => {

                setIsLoading(false);

                console.log(response);

                if (response.data.error) {
                    setNotice("Please, provide a file with a valid extension: pdf, csv, xls, xlsx, doc, docx, txt; max size: 20 Mb.");
                } else {
                    setNotice(response.data);
                }

                fetchUserFiles();
            })
            .catch(error => {

                setIsLoading(false);

                //setNotice(error);

                console.error(error);

            });
    };

    return (
        <>

            <form onSubmit={handleSubmit}>
                <input
                    type="file"
                    onChange={(e) => setFile(e.target.files[0])}
                />
               
                    {file && (
                        <button type="submit">Upload and process</button>
                    )}
            </form>

            {isLoading ? (
                <div className="loader"></div>
            ) : (
                    <p></p>
            )}

            {notice ? (
                <p>{notice}</p>
            ) : (
                    <p></p>
            )}
        </>
        
    );
};

export default FileUploadForm;
