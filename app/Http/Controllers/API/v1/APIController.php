<?php

namespace App\Http\Controllers\API\v1;

use Illuminate\Http\Request;
use App\Models\User;
use App\HTTP\Controllers\Controller;

class APIController extends Controller
{
    public function index($userId)
    {
        $user = User::findOrFail($userId);

        $filenames = $user->files()->pluck('filename')->toArray();

        return response()->json(['filenames' => $filenames]);
    }

}