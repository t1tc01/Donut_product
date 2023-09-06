'use client'
import React, { useState } from 'react';
// import Image from 'next/image'
import { Button } from 'antd';
import { UploadOutlined } from '@ant-design/icons'

export default function Home() {
  const [pathImage, setPathImage] = useState<File | null>(null);
  const [resultJson, setResultJson] = useState('Phan Hoàng Gay');

  return (
    <div
      className='flex h-screen bg-blue-100'
    >
      <div
        className='w-[50%] h-full border-[1px] border-black p-2 space-y-2'
      >
        <div
          className='w-full'
        >
          <input
            id={'input image'}
            onChange={e => {
              const files = e.target.files?.[0];
              if (files) {
                setPathImage(files);
              }
            }}
            type='file'
            className='hidden'
            accept='image/*'
          />
          <Button
            children='Upload image'
            onClick={(e) => {
              document.getElementById('input image')?.click()
            }}
            className='bg-blue-500 text-white'
            icon={<UploadOutlined />}
          />
        </div>
        <img
          src={pathImage != null ? URL.createObjectURL(pathImage) : undefined}
          alt=''
          className='w-full'
        />
      </div>

      <div
        className='w-[50%] h-full border-[1px] border-black space-x-2'
      >
        <div
          className='flex flex-col items-center'
        >
          Show result json here
        </div>

        <p>{resultJson}</p>
      </div>
    </div>
  )
}
