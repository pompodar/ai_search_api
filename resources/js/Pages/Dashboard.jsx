import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout';
import { Head } from '@inertiajs/react';
import { Link } from '@inertiajs/react'

export default function Dashboard({ auth }) {
    return (
        <AuthenticatedLayout
            user={auth.user}
        >
            {/* <Head title="Dashboard" /> */}

            <div className="py-12">
                <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">

                    <div className="bg-white overflow-hidden shadow-sm sm:rounded-lg p-4 w-48">

                        <Link className="p-6 text-gray-900" href="/my-data">My data</Link>

                    </div>

                    <div className="bg-white overflow-hidden shadow-sm sm:rounded-lg p-4 w-60 mt-4">

                        <Link className="p-6 text-gray-900" href="/testing-inviroment">Testing inviroment</Link>

                    </div>

                </div>
            </div>
        </AuthenticatedLayout>
    );
}
