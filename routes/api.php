<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\FileController;
use Illuminate\Support\Facades\Auth;
use App\Http\Controllers\API\v1\APIController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::middleware('web')->get('/refresh_dialog', [APIController::class, 'refresh_dialog']);

Route::middleware('web')->get('/get_token', [APIController::class, 'get_token']);

Route::middleware('web')->get('/get_user_id', function (Request $request) {
    return response()->json(['user_id' => $request->user()->id]);
});

Route::middleware(['auth:sanctum'])->post('/{userId}/search', [APIController::class, 'search']);

Route::middleware(['auth:sanctum'])->withoutMiddleware('csrf')->post('/test', function (Request $request) {
    $input1 = $request->input('input1');
    return $request;
});