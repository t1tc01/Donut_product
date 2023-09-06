'use client'
import React, { useRef, useState } from 'react'
import Image from 'next/image'
import { Button } from 'antd'


export default function Home() {
  const hiddenInputUpload = useRef(null);

  const [pathImage, setPathImage] = useState<File | null>(null);

  return (
    <div
      className='flex h-full w-full'
    >
      <div
        className='w-[50%] h-full border-[1px] border-black'
      >
        <div
          className='w-full'
        >
          <input
            ref={hiddenInputUpload}
            onChange={e => {
              const files = e.target.files?.[0];
              if(files) {
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
              if (hiddenInputUpload && hiddenInputUpload.current) {
                hiddenInputUpload?.current?.click()
              }
            }}
          />
        </div>
        <Image
          src={pathImage ? URL.createObjectURL(pathImage) : ''}
          alt=''
          width={500}
          height={500}
          className='w-full h-full'
        />
      </div>

      <div
        className='w-[50%] h-full flex justify-center'
      >
        show result json here
      </div>
    </div>
  )
}
