import React, { useState, useEffect } from 'react';
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
import { Head } from '@inertiajs/react';
import FileUploadForm from './Profile/Partials/FileUploadForm';
import axios from 'axios';
import { Viewer, Worker } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
import Modal from 'react-modal';
import { AiOutlineDelete } from "react-icons/ai";
import { AiFillFilePdf } from "react-icons/ai";

Modal.setAppElement('#app'); // Set the app element for accessibility

export default function FileUpload({ auth }) {
    const [userFiles, setUserFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const [isLoading, setIsLoading] = useState(false);

    const [notice, setNotice] = useState("");

    const [userId, setUserId] = useState("");

    const fetchUserFiles = async () => {
        try {
            const response = await axios.get('/user/files');
            setUserFiles(response.data.files);
        } catch (error) {
            console.error('Error fetching user files:', error);
        }
    };

    useEffect(() => {
        getUserID();
    }, []);

    const getUserID = async () => {
        try {
            const response = await axios.get('/api/get_user_id');
            setUserId(response.data.user_id);
        } catch (error) {
            console.error('Error fetching user files:', error);
        }
    };

    const handleFileSelect = (file) => {
        setSelectedFile(file);
        setIsModalOpen(true); // Open the modal when a file is selected
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setSelectedFile(null); // Reset selected file when modal is closed
    };

    const handleDeleteFile = async (fileId) => {
        const confirmed = window.confirm('Are you sure you want to delete this file?');
        
        if (!confirmed) {
            return;
        }

        setNotice("");

        setIsLoading(true);

        try {
            const response = await axios.delete(`/user/${auth.user.id}/files/${fileId}`);
            
            fetchUserFiles();

            setNotice(response.data);

            setIsLoading(false);

        } catch (error) {
            console.error('Error deleting file:', error);

            setNotice(error);

            setIsLoading(false);

        }
    };

    return (
        <AuthenticatedLayout user={auth.user}>
            <Head title="FileUpload" />

            <div className="py-12">
                <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">

                    {userFiles.length == 0 ? (

                        <>

                            <h1>You can upload up to 5 files. Valid extensions: pdf, csv, doc, docx, txt; max size: 20 Mb</h1>

                            <FileUploadForm fetchUserFiles={fetchUserFiles} notice={notice} setNotice={setNotice}/>

                        </>
                    
                    ) : (

                        <>

                            {userFiles.length < 5 ? (

                            <>

                                <h1>You can upload up to 5 files. Valid extensions: pdf, csv, doc, docx, txt; max size: 20 Mb</h1>

                                <FileUploadForm fetchUserFiles={fetchUserFiles} />

                            </>

                            ) : (

                                <h1>To change your data you have to first remove some file/files you already uploaded.</h1>

                            ) }
                            

                            <h2 className="flex justify-center mt-4">Uploaded File</h2>
                            <ul className="user-files-list flex justify-center gap-4">
                                {userFiles.map((file, index) => (
                                    <li className="user-files__item" key={index}>
                                        
                                        {/* <button className="user-files-view-icon text-sm" onClick={() => handleFileSelect(file)}> */}

                                        <p className="user-files-view-icon text-sm text-center" >

                                            <AiFillFilePdf />
                                            
                                            {file.filename}
                                            
                                        </p>
                                        
                                        <button className="user-files-delete-icon" onClick={() => handleDeleteFile(file.id)}>
                                    
                                            <AiOutlineDelete />

                                        </button>

                                    </li>
                                ))}
                            </ul>

                            <p>Your user id: {userId}</p>

                            <p>Your secret key: {notice}</p>

                            <hr></hr>

                            <p>
                                Here is an example of code you can use:
                            </p>

                            <hr></hr>


                            <code>

                            {`<?php`}<br/>
                            {`$userId = <Your user id>;`}<br/>
                            {`$endpoint = "https://srv518474.hstgr.cloud/api/{$userId}/search/";`}<br/>
                            {`$token = <Your secret key>;`}<br/>
                            {`$history = isset($_COOKIE['history']) ? json_decode($_COOKIE['history'], true) : array();`}<br/>
                            {``}<br/>
                            {`// Check if the form is submitted`}
                            {`if ($_SERVER["REQUEST_METHOD"] == "POST") {`}<br/>
                            {`    if (isset($_POST['clear_history'])) {`}<br/>
                            {`        // Clear the history from cookies`}<br/>
                            {`        setcookie("history", "", time() - 3600, "/"); // set to a past time to expire the cookie`}<br/>
                            {``}<br/>
                            {`        $history = array(); `}<br/>
                            {`    } else {`}<br/>
                            {`        // Retrieve form data`}<br/>
                            {`        $prompt = $_POST['prompt'];`}<br/>
                            {`        $question = $_POST['question'];`}<br/>
                            {``}<br/>
                            {`        // Prepare the data payload`}<br/>
                            {`        $data = array(`}<br/>
                            {`            'prompt' => $prompt,`}<br/>
                            {`            'question' => $question,`}<br/>
                            {`            'history' => $history`}<br/>
                            {`        );`}<br/>
                            {`    `}<br/>
                            {`    $ch = curl_init();`}<br/>
                            {``}<br/>
                            {`    // Set the URL`}<br/>
                            {`    curl_setopt($ch, CURLOPT_URL, $endpoint);`}<br/>
                            {``}<br/>
                            {`    // Set the request method (GET, POST, PUT, DELETE, etc.)`}<br/>
                            {`    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');`}<br/>
                            {``}<br/>
                            {`    // Set the Authorization header with the Bearer token`}<br/>
                            {`    curl_setopt($ch, CURLOPT_HTTPHEADER, array(`}<br/>
                            {`        'Authorization: Bearer ' . $token,`}<br/>
                            {`    ));`}<br/>
                            {``}<br/>
                            {`    // Set the data to be sent`}<br/>
                            {`    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));`}<br/>
                            {``}<br/>
                            {`    // Set to receive the response as a string`}<br/>
                            {`    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);`}<br/>
                            {``}<br/>
                            {`    // Execute the request`}<br/>
                            {`    $response = curl_exec($ch);`}<br/>
                            {``}<br/>
                            {`    // Check for errors`}<br/>
                            {`    if (curl_errno($ch)) { `}<br/>
                            {`        echo 'Curl error: ' . curl_error($ch);`}<br/>
                            {`    }`}<br/>
                            {``}<br/>
                            {`    // Close cURL session`}<br/>
                            {`    curl_close($ch);`}<br/>
                            {``}<br/>
                            {`    $history[] = array('question' => $question, 'response' => $response);`}<br/>
                            {``}<br/>
                            {`    // Store the updated history in cookies`}<br/>
                            {`    setcookie("history", json_encode($history), time() + (86400 * 30), "/"); // 86400 = 1 day`}<br/>
                            {`}<br/>`}<br/>
                            {`?>`}<br/>
                            {``}<br/>
                            {`<!DOCTYPE html>`}<br/>
                            {`<html>`}<br/>
                            {`<head>`}<br/>
                            {`    <title>Form with cURL</title>`}<br/>
                            {`</head>`}<br/>
                            {`<body>`}<br/>
                            {`    <?php`}<br/>
                            {`        if (!empty($history)) { `}<br/>
                            {`            echo "<h2>History:</h2>";`}<br/>
                            {`            echo "<ul>";`}<br/>
                            {`            foreach ($history as $entry) { `}<br/>
                            {`                echo "<li><strong>Question:</strong> " . $entry['question'] . "<br/>";`}<br/>
                            {`                echo "<strong>Response:</strong> " . $entry['response'] . "</li>";`}<br/>
                            {`            }`}<br/>
                            {`            echo "</ul>";`}<br/>
                            {`        }`}<br/>
                            {`    ?>`}<br/>
                            {`    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">`}<br/>
                            {`        Prompt: <input type="text" name="prompt"><br/><br/>`}<br/>
                            {`        Question: <input type="text" name="question"><br/><br/>`}<br/>
                            {`        <input type="submit" value="Submit">`}<br/>
                            {`    </form>`}<br/>
                            {``}<br/>
                            {`    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">`}<br/>
                            {`        <input type="hidden" name="clear_history" value="true">`}<br/>
                            {`        <button type="submit">Clear History</button>`}<br/>
                            {`    </form>`}<br/>
                            {`</body>`}<br/>
                            {`</html>`}<br/>

                                
                            </code>
                        
                        </>
                        
                    )}

                    <Modal
                        isOpen={isModalOpen}
                        onRequestClose={closeModal}
                        contentLabel="PDF Viewer Modal"
                    >
                        
                        {selectedFile && (
                            <div className="">
                                <h2 className="flex items-center justify-center mb-2 font-bold">{selectedFile.filename}</h2>
                                <Worker workerUrl="./pdfjs/pdf.worker.min.js">
                                    <Viewer fileUrl={`/storage/users-files/user-${auth.user.id}/${selectedFile.filename}`} />
                                </Worker>
                            </div>
                        )}
                    </Modal>
                </div>

                {isLoading ? (
                    <div className="loader"></div>
                ) : (
                        <p></p>
                )}

            </div>
        </AuthenticatedLayout>
    );
}
