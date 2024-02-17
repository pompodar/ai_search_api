import React, { useState, useEffect } from 'react';
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
import { Head } from '@inertiajs/react';
import FileUploadForm from './Profile/Partials/FileUploadForm';
import axios from 'axios';
import { Viewer, Worker } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';

export default function UserFile({ auth }) {
    const [userFiles, setUserFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);

    useEffect(() => {
        fetchUserFiles();
    }, []);

    const fetchUserFiles = async () => {
        try {
            const response = await axios.get('/user/files');
            setUserFiles(response.data.files);
        } catch (error) {
            console.error('Error fetching user files:', error);
        }
    };

    const handleFileSelect = (file) => {
        setSelectedFile(file);
    };

    const handleDeleteFile = async (fileId) => {
        const confirmed = window.confirm('Are you sure you want to delete this file?');
        
        if (!confirmed) {
            return;
        }

        try {
            await axios.delete(`/user/${auth.user.id}/files/${fileId}`);
            
            fetchUserFiles();

        } catch (error) {
            console.error('Error deleting file:', error);
        }
    };

    return (
        <AuthenticatedLayout user={auth.user}>
            <Head title="FileUpload" />

            <div className="py-12">
                <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
                    <h2>Upload PDF</h2>
                    <FileUploadForm fetchUserFiles={ fetchUserFiles } />

                    <h2>Uploaded Files</h2>
                    <ul>
                        {userFiles.map((file, index) => (
                            <li key={index}>
                                <span onClick={() => handleFileSelect(file)}>{file.path}</span>
                                <button onClick={() => handleDeleteFile(file.id)}>Delete</button>
                            </li>
                        ))}
                    </ul>

                    {selectedFile && (
                        <div className="mt-4">
                            <h2>Selected File Content</h2>
                            <Worker workerUrl="./pdfjs/pdf.worker.min.js">
                                <Viewer fileUrl={`/storage/users-files/${auth.user.id}/${selectedFile.filename}`} />
                            </Worker>
                        </div>
                    )}
                </div>
            </div>
        </AuthenticatedLayout>
    );
}
