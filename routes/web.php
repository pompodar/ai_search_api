<?php

use App\Http\Controllers\ProfileController;
use Illuminate\Foundation\Application;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;
use App\Http\Controllers\FileController;
use App\Http\Controllers\API\v1\APIController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return Inertia::render('Welcome', [
        'canLogin' => Route::has('login'),
        'canRegister' => Route::has('register'),
        'laravelVersion' => Application::VERSION,
        'phpVersion' => PHP_VERSION,
    ]);
});

Route::get('/dashboard', function () {
    return Inertia::render('Dashboard');
})->middleware(['auth', 'verified'])->name('dashboard');

Route::get('/my-data', function () {
    return Inertia::render('UserData');
})->middleware(['auth', 'verified'])->name('user_data');

Route::get('/testing-inviroment', function () {
    return Inertia::render('TestingInviroment');
})->middleware(['auth', 'verified'])->name('testing_inviroment');

Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});

Route::middleware(['auth', 'verified'])->post('/file/upload_and_ingest', [FileController::class, 'upload_and_ingest']);

Route::middleware(['auth', 'verified'])->get('/user/files', [FileController::class, 'getUserFiles']);

Route::middleware(['auth', 'verified'])->delete('/user/{userId}/files/{fileId}', [FileController::class, 'deleteFile']);

Route::middleware(['auth', 'verified'])->get('/process', [FileController::class, 'process']);

Route::middleware(['auth', 'verified'])->post('/search', [FileController::class, 'search']);

Route::middleware(['auth', 'verified', 'auth:sanctum'])->group(function () {
    Route::get('/user/{userId}/{question}', [APIController::class, 'search']);
});

Route::get('test', function () {
    echo 3;
})->middleware('auth:sanctum');

require __DIR__.'/auth.php';