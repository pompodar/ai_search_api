import React, { useState, useEffect } from 'react';
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
import { Head } from '@inertiajs/react';
import FileUploadForm from './Profile/Partials/FileUploadForm';
import axios from 'axios';

export default function FileUpload({ auth }) {
    const [userFiles, setUserFiles] = useState([]);

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

    return (
        <AuthenticatedLayout
            user={auth.user}
            // header={<h2 className="font-semibold text-xl text-gray-800 leading-tight">Dashboard</h2>}
        >
            <Head title="FileUpload" />

            <div className="py-12">
                <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
                    <h2>Upload PDF</h2>
                    <FileUploadForm />

                    <h2>Uploaded Files</h2>
                    <ul>
                        {userFiles.map((file, index) => (
                            <li key={index}>{file.path}</li>
                        ))}
                    </ul>
                </div>
            </div>
        </AuthenticatedLayout>
    );
}
