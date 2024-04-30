<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\FileController;
use Illuminate\Support\Facades\Auth;

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

Route::middleware('web')->get('/hi', function (Request $request) {
    $user = $request->user();

    // Ensure the user is authenticated
    if (!$user) {
        return response()->json(['error' => 'Unauthorized'], 401);
    }

    // Generate a personal access token for the authenticated user
    $tokenName = 'test'; // Replace 'YourTokenName' with your desired token name
    $token = $user->createToken($tokenName);

    // foreach ($user->tokens as $token) {
    //     echo $token;
    // }

    // Return the generated token
    return ['token' => $token->plainTextToken];
});

Route::middleware(['web', 'auth:sanctum'])->get('/test', function (Request $request) {

    return ['test' => 'test'];
});