<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Models\UserFile;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

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

        $uploadedFile = $request->file('pdf');
        $originalFilename = $uploadedFile->getClientOriginalName();

        $fileName = $originalFilename;
        $fileCounter = 1;

        while (Storage::disk('local')->exists("public/users-files/user-{$user->id}/$fileName")) {

            $fileName = pathinfo($originalFilename, PATHINFO_FILENAME) . '_' . $fileCounter . '.' . $uploadedFile->getClientOriginalExtension();
            $fileCounter++;
        }

        $path = $uploadedFile->storeAs("public/users-files/user-{$user->id}", $fileName);

        $file = new UserFile(['path' => $path, 'filename' => $fileName]);
        
        $user->files()->save($file);

        return response()->json(['path' => $path, 'filename' => $fileName]);
    }

    public function deleteFile($userId, $fileId)
    {

        $user = Auth::user();
        
        $file = $user->files()->where('id', $fileId)->firstOrFail();

        Storage::delete($file->path);

        $file->delete();

        return response()->json(['message' => 'File deleted successfully']);
    }

    public function getUserFiles()
    {
        $userFiles = Auth::user()->files()->get();

        return response()->json(['files' => $userFiles]);
    }

    public function show($filename)
    {
        $file = Storage::disk('local')->path($filename);
        return response()->file($file);
    }

    public function process()
    {
        $userId = Auth::id();

        $pdfsPath = public_path(). "\storage\users-files\p1\user-" . $userId;

        $pythonScriptPath = app_path(). '\ai\ingest.py';

        $process = new Process(['C:\Users\User\AppData\Local\Programs\Python\Python39\python.exe', $pythonScriptPath, $pdfsPath]);
        
        $command = '"' . 'C:\Users\User\AppData\Local\Programs\Python\Python39\python.exe' . '" "' . $pythonScriptPath . '" "' . $pdfsPath . '"';

        exec($command, $output, $returnCode);

        dd($output );

        // $process->run();

        // if (!$process->isSuccessful()) {
        //     throw new ProcessFailedException($process);
        // }

        // // Return the output as JSON response
        // return response()->json(['output' => $process->getOutput()]);
    }
}