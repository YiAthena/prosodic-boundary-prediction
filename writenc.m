function writenc( onehotfile, prosodyfile, framefile, nc_filename )

    onehot = load(onehotfile);
    prosody = load(prosodyfile);
    frame = load(framefile);
	%onehot = int8(onehot);
	%prosody = int8(prosody);

    numSeqs = size(frame,1);
    numTimesteps = sum(frame);
    inputPattSize = size(onehot,2);
    targetPattSize = size(prosody,2);
    maxSeqTagLength = 5;

    ncid = netcdf.create(nc_filename,'NETCDF4');
    %netcdf.setDefaultFormat('NC_FORMAT_64BIT');

    numSeqsId = netcdf.defDim(ncid,'numSeqs',numSeqs);
    numTimestepsId = netcdf.defDim(ncid,'numTimesteps',numTimesteps);
    inputPattSizeId = netcdf.defDim(ncid,'inputPattSize',inputPattSize);
    maxSeqTagLengthId = netcdf.defDim(ncid,'maxSeqTagLength',maxSeqTagLength);
    targetPattSizeId = netcdf.defDim(ncid,'targetPattSize',targetPattSize);
    
    seqTagsID = netcdf.defVar(ncid,'seqTags','char',[maxSeqTagLengthId numSeqsId]);
    seqLengthsID = netcdf.defVar(ncid,'seqLengths','int',numSeqsId);
    inputsID = netcdf.defVar(ncid,'inputs','float',[inputPattSizeId numTimestepsId]);
    targetPatternsID = netcdf.defVar(ncid,'targetPatterns','float',[targetPattSizeId numTimestepsId]);
    netcdf.endDef(ncid);
    
    frameIndex = 0;
    fileIndex = 0;
    cnt = 10000;
    for i=1:numSeqs
        D = onehot(frameIndex+1:frameIndex+frame(i),:);
        B = prosody(frameIndex+1:frameIndex+frame(i),:);
        
        netcdf.putVar(ncid,inputsID,[0 frameIndex],[size(D,2) size(D,1)],D');
        netcdf.putVar(ncid,targetPatternsID,[0 frameIndex],[size(B,2) size(B,1)],B');

        netcdf.putVar(ncid,seqTagsID,[0 fileIndex],[length(int2str(cnt)) 1],int2str(cnt));
        netcdf.putVar(ncid,seqLengthsID,fileIndex,1,size(D,1));
        cnt = cnt + 1;
        fileIndex = fileIndex + 1;
        frameIndex = frameIndex + size(D,1);
    end
    netcdf.close(ncid);
end

