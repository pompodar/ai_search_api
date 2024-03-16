<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class UserFile extends Model
{
    protected $fillable = ['path', 'filename'];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}