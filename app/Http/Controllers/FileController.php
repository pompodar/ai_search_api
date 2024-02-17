<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Models\UserFile;

class FileController extends Controller
{
    public function upload(Request $request)
    {
        
        if (!Auth::check()) {
            return response()->json(['error' => 'Unauthorized'], 401);
        }

        $request->validate([
            'pdf' => 'required|mimes:pdf|max:2048',
        ]);

        $user = Auth::user();

        $path = $request->file('pdf')->store("users-files/{$user->id}");

        $file = new UserFile(['path' => $path]);
        
        $user->files()->save($file);

        return response()->json(['path' => $path]);
    
    }

    public function getUserFiles()
    {
        $userFiles = Auth::user()->files()->get();

        return response()->json(['files' => $userFiles]);
    }

}