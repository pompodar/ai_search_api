import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FileUploadForm = ({ fetchUserFiles, notice, setNotice }) => {

    const [isLoading, setIsLoading] = useState(false);

    const [file, setFile] = useState(null);

    useEffect(() => {
        getToken();
    }, []);

    const getToken = () => {
        axios.get('/api/get_token')
        .then(response => {

            console.log(response);

            if (response.data.error) {
                setNotice("Something went wrong. We cannot get your token.");
            } else {
                setNotice(response.data.token);
                console.log(response.data.user_id);
            }

            fetchUserFiles();
        })
        .catch(error => {

            setIsLoading(false);

            //setNotice(error);

            console.error(error);

        });
    }

    const handleSubmit = (e) => {
        e.preventDefault();

        setIsLoading(true);

        const formData = new FormData();
        formData.append('file', file);

        axios.post('/file/upload_and_ingest', formData)
            .then(response => {

                setIsLoading(false);

                console.log(response);

                if (response.data.error) {
                    setNotice("Please, provide a file with a valid extension: pdf, csv, doc, docx, txt; max size: 20 Mb.");
                } else {
                    setNotice(response.data.token);
                    console.log(response.data.token);
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
        </>
        
    );
};

export default FileUploadForm;
