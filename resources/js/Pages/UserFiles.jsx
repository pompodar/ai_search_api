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
                    <FileUploadForm fetchUserFiles={fetchUserFiles} />

                    <h2 class="flex justify-center mt-4">Uploaded Files</h2>
                    <ul className="user-files-list flex justify-center gap-4">
                        {userFiles.map((file, index) => (
                            <li class="user-files__item" key={index}>
                                
                                <button className="user-files-view-icon text-sm" onClick={() => handleFileSelect(file)}>

                                    <AiFillFilePdf />
                                    
                                    {file.filename}
                                    
                                </button>
                                
                                <button class="user-files-delete-icon" onClick={() => handleDeleteFile(file.id)}>
                            
                                    <AiOutlineDelete />

                                </button>

                            </li>
                        ))}
                    </ul>

                    <Modal
                        isOpen={isModalOpen}
                        onRequestClose={closeModal}
                        contentLabel="PDF Viewer Modal"
                    >
                        {selectedFile && (
                            <div className="">
                                <h2 class="flex items-center justify-center mb-2 font-bold">{selectedFile.filename}</h2>
                                <Worker workerUrl="./pdfjs/pdf.worker.min.js">
                                    <Viewer fileUrl={`/storage/users-files/user-${auth.user.id}/${selectedFile.filename}`} />
                                </Worker>
                            </div>
                        )}
                    </Modal>
                </div>
            </div>
        </AuthenticatedLayout>
    );
}
