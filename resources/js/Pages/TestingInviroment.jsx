import React, { useState, useEffect } from 'react';
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
import { Head } from '@inertiajs/react';
import axios from 'axios';
import Modal from 'react-modal';

Modal.setAppElement('#app'); // Set the app element for accessibility

export default function FileUpload({ auth }) {
    const [userFiles, setUserFiles] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        fetchUserFiles();
    }, []);

    const fetchUserFiles = async () => {
        try {
            const response = await axios.get('/user/files');
            setUserFiles(response.data.files);
            console.log('there are some files');
        } catch (error) {
            console.error('Error fetching user files:', error);
        }
    };

    const closeModal = () => {
        setIsModalOpen(false);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setIsLoading(true);
        const formData = new FormData();
        formData.append('question', question);
        axios.post('/search', formData)
            .then(response => {
                setIsLoading(false);
                setAnswer(response.data);
            })
            .catch(error => {
                setIsLoading(false);
                console.error('Error:', error);
                setAnswer("An error occurred while processing your request.");
            });
    };

    return (
        <AuthenticatedLayout user={auth.user}>
            <Head title="TestingInviroment" />
            <div className="py-12">
                <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
                    <h1>Testing Inviroment</h1>
                    {userFiles.length > 0 ? (
                        <form onSubmit={handleSubmit} className="mt-4 flex flex-col">
                            <label className="flex flex-col">
                                Enter your question:
                                <textarea type="text" name="question" onChange={(e) => setQuestion(e.target.value)}></textarea>
                            </label>
                            <button type="submit">Submit</button>
                        </form>
                    ) : (
                        <p>You have not uploaded any files yet.</p>
                    )}
                    {isLoading ? (
                        <div className="loader"></div>
                    ) : (
                        answer ? (
                            <p className="mt-4">{answer}</p>
                        ) : null
                    )}
                </div>
            </div>
        </AuthenticatedLayout>
    );
}
